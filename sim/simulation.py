from typing import Any, Dict, Generator, List
import numpy as np
from .body import Body
from .integrator import compute_accelerations, leapfrog_step
from .collision import check_collisions


def run(bodies: List[Body], dt: float, total_time: float, every: int = 1) -> Generator[Dict[str, Any], None, None]:
    """
    Generator that yields one frame dict per recorded step.

    Each yielded dict:
        {
            "positions": [[x, y, z], ...],   # one per body, metres
            "collision": None | {"frame": int, "body_a": int, "body_b": int, "names": [str, str]}
        }

    On collision: emits the final frame with collision data, then returns.
    """
    n_steps = int(total_time / dt)
    acc = compute_accelerations(bodies)
    frame_index = 0

    for step in range(n_steps):
        acc = leapfrog_step(bodies, acc, dt)

        if (step + 1) % every == 0:
            positions = [body.position.tolist() for body in bodies]
            collision = check_collisions(bodies)

            if collision is not None:
                i, j = collision
                yield {
                    "positions": positions,
                    "collision": {
                        "frame": frame_index,
                        "body_a": i,
                        "body_b": j,
                        "names": [bodies[i].name, bodies[j].name],
                    },
                }
                return

            yield {"positions": positions, "collision": None}
            frame_index += 1
