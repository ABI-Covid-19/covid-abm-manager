from .agent import Agent
from .store_shelves import StoreShelf
from ..state.agent_state import State
from ..data.agent_data import DataRep

import numpy as np


class ShopperInstance(type):
    def __instancecheck__(self, other):
        if other == Shopper:
            return True
        else:
            return False


class Shopper(Agent, metaclass=ShopperInstance):

    __id__ = 0

    def __init__(self, model, position, exit_cell, state=State.HEALTHY, social_distancing=False):

        shopper_id = Shopper.__id__
        Shopper.__id__ += 1

        super().__init__(shopper_id, model)

        #  model attributes
        self.model = model
        self.model_space = self.model.space

        #  agent attributes
        self.pos = position
        self.state = state
        self.social_distancing = social_distancing
        self.exit_time = np.random.randint(120, 240)
        self.exit_timer = 0
        self.exit = exit_cell
        self.at_risk_timer = 0
        self.remove_timer = 0

        self.removed = False

    @property
    def random(self):
        return self.model.random

    def step(self):
        self._move()
        self._infect()
        self._check_expose()
        self._check_remove()

    def _move(self):
        """
        Move an agent.

        :return:
        """
        if self.removed:
            return

        all_neighbours = self._get_neighbours()
        shelf_neighbours = list()
        customer_neighbours = list()
        for neighbour in all_neighbours:
            if isinstance(neighbour, StoreShelf):
                shelf_neighbours.append(neighbour.pos)
            elif isinstance(neighbour, StoreShelf):
                customer_neighbours.append(neighbour.pos)

        speed = np.random.randint(1, 3)
        heading = np.random.random(2) * 2 - 1
        heading = heading / np.linalg.norm(heading)  # normalising the heading vector
        new_pos = self.pos + (heading * speed)  # new position obtained speed and heading.

        while (tuple(new_pos.tolist()) in shelf_neighbours) and (tuple(new_pos.tolist()) in customer_neighbours):
            heading = np.random.random(2) * 2 - 1
            heading = heading / np.linalg.norm(heading)
            new_pos = self.pos + (heading * speed)

        #  when shopper does not practice social distancing
        if not self.social_distancing:
            self.model_space.move_agent(self, new_pos)

        #  when shopper does social distancing (considering the are aren't other shoppers withing 2m distance)
        if self.social_distancing and (len(customer_neighbours) == 0):
            self.model_space.move_agent(self, new_pos)

    # TODO: Surface transmission

    def _get_neighbours(self):
        all_neighbours = self.model.space.get_neighbors(
            self.pos,
            1.0,
            include_center=False
        )
        return all_neighbours

    def _check_expose(self):
        """
        If a "risky" shopper is in close contact with an infected shopper, he/she becomes "exposed".

        :return:
        """

        if self.pos is None:
            return

        if self.state == State.RISKY:
            neighbours = self._get_neighbours()
            if len(neighbours) > 0:
                for shopper in neighbours:
                    if not isinstance(shopper, StoreShelf):
                        #  if the risky shopper is in close contact with an infected shopper for more than 3 min,
                        #  then the risky shopper becomes exposed.
                        if shopper.state == State.INFECTED:
                            self.at_risk_timer += 1
                            if self.at_risk_timer == 9:
                                self.state = State.EXPOSED

    def _check_remove(self):
        self.exit_timer += 1
        if self.exit_timer == self.exit_time:
            print("Agent {} removed after {} times".format(self.unique_id, self.exit_time))
            self.model.space.remove_agent(self)
            self.removed = True

    def _infect(self):
        """
        If the current shopper is nearby an infected shopper, he/she becomes "risky".

        :return:
        """

        if self.state == State.INFECTED:
            return

        if self.pos is None:
            return

        neighbours = self._get_neighbours()
        if len(neighbours) > 0:
            for shopper in neighbours:
                if not isinstance(shopper, StoreShelf):
                    if shopper.state == State.INFECTED:
                        self.state = State.RISKY
                        break

    def collect_data(self, step=0) -> DataRep:
        if self.removed:
            data = DataRep(
                **{
                    "step": step,
                    "unique_id": self.unique_id,
                    "state": self.state,
                    "x": None,
                    "y": None,
                    "social_distancing": self.social_distancing,
                }
            )
        else:
            data = DataRep(
                **{
                    "step": step,
                    "unique_id": self.unique_id,
                    "state": self.state,
                    "x": self.pos[0] + 0.5,
                    "y": self.pos[1] + 0.5,
                    "social_distancing": self.social_distancing,
                }
            )
        return data
