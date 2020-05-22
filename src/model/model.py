import time
import random


class Model:
    """
    Base class for all agent based models.
    """

    def __new__(cls, *args, **kwargs):
        """
        Create a new model object.
        """

        model = object.__new__(cls)
        model._seed = time.time()
        if "seed" in kwargs and kwargs["seed"] is not None:
            model._seed = kwargs["seed"]
        model.random = random.Random(model._seed)
        return model

    def __init__(self):
        """
        Create a new model.
        """

        self.running = True
        self.schedule = None
        self.current_id = 0
        self._seed = None

    def run_model(self):
        """
        Run the model until the end condition is reached.
        """
        while self.running:
            self.step()

    def step(self):
        """
        A single step.
        """
        pass

    def next_id(self):
        """
        Return the next unique ID for agents, increment current_id
        """
        self.current_id += 1
        return self.current_id

    def reset_randomizer(self, seed=None):
        """
        Reset the model random number generator.

        :param seed: A new seed for the RNG; if None, reset using the current seed
        :return:
        """

        if seed is None:
            seed = self._seed
        self.random.seed(seed)
        self._seed = seed
