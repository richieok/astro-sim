from dataclasses import dataclass, field
import numpy as np


@dataclass
class Body:
    name: str
    mass: float          # kg
    radius: float        # metres (for collision math)
    radius_km: float     # km (for display)
    color: str           # hex e.g. "#FFD700"
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))  # shape (3,), metres
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))  # shape (3,), m/s
