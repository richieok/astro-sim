import numpy as np
from typing import List
from .body import Body

G = 6.674e-11  # gravitational constant, SI


def compute_accelerations(bodies: List[Body]) -> np.ndarray:
    """Compute gravitational accelerations for all bodies (O(N²) all-pairs)."""
    n = len(bodies)
    acc = np.zeros((n, 3))
    for i in range(n):
        for j in range(i + 1, n):
            r = bodies[j].position - bodies[i].position
            dist = np.linalg.norm(r)
            if dist == 0:
                continue
            force_dir = r / dist
            mag = G / (dist * dist)
            acc[i] += mag * bodies[j].mass * force_dir
            acc[j] -= mag * bodies[i].mass * force_dir
    return acc


def leapfrog_step(bodies: List[Body], acc: np.ndarray, dt: float) -> np.ndarray:
    """Perform one leapfrog (velocity-Verlet) step. Returns updated accelerations."""
    # Half-kick: v += 0.5 * acc * dt
    for i, body in enumerate(bodies):
        body.velocity += 0.5 * acc[i] * dt

    # Drift: x += v * dt
    for body in bodies:
        body.position += body.velocity * dt

    # Recompute accelerations
    acc_new = compute_accelerations(bodies)

    # Half-kick: v += 0.5 * acc_new * dt
    for i, body in enumerate(bodies):
        body.velocity += 0.5 * acc_new[i] * dt

    return acc_new
