import enum


class State(enum.Enum):
    HEALTHY = "Healthy"
    INFECTED = "Infected"
    RISKY = "Risky"
    EXPOSED = "Exposed"
