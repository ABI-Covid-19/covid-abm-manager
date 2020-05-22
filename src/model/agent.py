class Agent:
    """
    Base class for a model agent.
    """

    def __init__(self, unique_id, model):
        """
        Create a new agent.
        """
        self.unique_id = unique_id
        self.model = model

    def step(self):
        """
         single step of the agent.
         """
        pass

    @property
    def random(self):
        return self.model.random
