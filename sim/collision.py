from typing import List, Optional, Tuple
from .body import Body


def check_collisions(bodies: List[Body]) -> Optional[Tuple[int, int]]:
    """Check all pairs for collision. Returns (i, j) indices if collision found, else None."""
    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            r = bodies[j].position - bodies[i].position
            dist = (r[0]**2 + r[1]**2 + r[2]**2) ** 0.5
            if dist < bodies[i].radius + bodies[j].radius:
                return (i, j)
    return None
