from dataclasses import dataclass

from state.agent_state import State


@dataclass
class DataRep:
    """
    Wrapping a representative data from the simulation.
    """
    step: int
    unique_id: int
    state: State
    x: float
    y: float
    social_distancing: bool

    def __post_init__(self):
        """
        Converting to proper data format for later analysis.
        """
        self.social_distancing = int(self.social_distancing)
        self.state = self.state.value
