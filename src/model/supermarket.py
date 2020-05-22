from model.model import Model
from model.store_shelves import StoreShelf
from model.utils.store import Store
from model.shopper import Shopper
from state.agent_state import State

from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from dataclasses import asdict

import numpy as np
import pandas as pd

STORE_SIZES = dict(small=(70, 50),
                   medium=(100, 50),
                   large=(100, 80))


class SupermarketModel(Model):
    """
    The generic supermarket model using a continuous environment.
    """

    unique_id = 0

    def __init__(self, number_of_customers, number_of_infected, social_distance_prob=0.80,
                 size='small'):

        super(SupermarketModel).__init__()

        self._num_customers = number_of_customers
        self._num_infected = number_of_infected
        self._step_count = 0
        self._enter_time = 0

        #  store environment
        self.width, self.height = STORE_SIZES[size][0] // 2, STORE_SIZES[size][1] // 2
        floor_area = self.width * self.height
        #  TODO: Environment should become non-toroidal.
        self.space = ContinuousSpace(self.width, self.height, True)
        model_description = {  # this gets updated during store planning
            "area": floor_area,
            "width": self.width,
            "height": self.height,
        }
        self._store_environment = Store(model_description)
        self.shelves = self._store_environment.generate_store()
        self._generate_store_shelves()

        #  scheduler
        self.schedule = RandomActivation(self)
        if social_distance_prob > 1.0:
            social_distance_prob = social_distance_prob / 100
        self._social_distance_prob = social_distance_prob

        #  data collector
        self._simulated_dataset = pd.DataFrame()
        self.datacollector = DataCollector(
            {
                "Healthy": lambda m: self.count_agents_with_state(m, "Healthy"),
                "Risky": lambda m: self.count_agents_with_state(m, "Risky"),
                "Exposed": lambda m: self.count_agents_with_state(m, "Exposed"),
                "Infected": lambda m: self.count_agents_with_state(m, "Infected"),
            })

        #  add shoppers into the supermarket
        self.add_agents(self._num_customers, self._num_infected)
        self.running = True
        self.datacollector.collect(self)

    def _check_removed_agent(self):
        """
        Removes an agent from the model's space, once the agent is no longer in the store.

        :return:
        """
        for index in range(len(self.schedule.agents)):
            if self.schedule.agents[index].pos is None:
                self.schedule.agents.pop(index)

    def _generate_store_shelves(self):
        """
        Generates the shelves in the store. The coordinates of these shelves will be marked on the model's space.
        Agents cannot move over these coordinates.

        :return:
        """
        for shelf in range(len(self.shelves)):
            pos = self.shelves[shelf]
            a = StoreShelf(shelf,
                           self,
                           pos=pos)
            self.space.place_agent(a, pos)

    def _save_data(self):
        """
        Fetches the collected data from DataRep, converts the into a dict type and then stores them as pandas DataFrame.
        :return:
        """
        self._check_removed_agent()
        self._simulated_dataset = self._simulated_dataset.append(
            pd.DataFrame(asdict(agent.collect_data(self._step_count)) for agent in self.schedule.agents),
            ignore_index=True)

    def add_agents(self, number_of_shoppers, number_of_infected):
        """
        Creates an instance of the Shopper class, and adds that (along with its attributes) into the model's space.

        :param number_of_shoppers:
        :param number_of_infected:
        :return:
        """
        for agent in range(number_of_shoppers):
            occupy_flag = True
            while occupy_flag:
                x = self.random.randrange(self.space.width)
                y = self.random.randrange(self.space.height)
                if (x, y) not in self.shelves:
                    position = (x, y)
                    occupy_flag = False
                    is_social_distancing = self.random.random() < self._social_distance_prob
                    a = Shopper(self,
                                position=position,
                                exit_cell=None,
                                social_distancing=is_social_distancing)

                    if agent <= number_of_infected:
                        a.state = State.INFECTED
                        is_social_distancing = self.random.random() < self._social_distance_prob
                        a.social_distancing = is_social_distancing

                    self.space.place_agent(a, (x, y))
                    self.schedule.add(a)

    @staticmethod
    def count_agents_with_state(model, state):
        """
        Helper method to count number of agents in a given state.

        :param model: model instance.
        :param state: given state.
        :return:
        """
        count = 0
        for agent in model.schedule.agents:
            if agent.state.value == state:
                count += 1
        return count

    def get_simulation_result(self):
        """
        Get the result from the simulation.
        :return:
        """
        return self._simulated_dataset

    def step(self):
        """
        Run the model with one step (day).
        """
        self._step_count += 1
        self._enter_time += 1
        self._save_data()
        self.schedule.step()
        self.datacollector.collect(self)

        if self._enter_time == 8:
            number_of_new_customers = np.random.randint(1, 5)
            is_infected = self.random.random() < 0.1
            if is_infected:
                number_of_new_infected = 1
            else:
                number_of_new_infected = 0
            self.add_agents(number_of_new_customers, number_of_new_infected)
            self._enter_time = 0
