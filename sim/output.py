import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from .body import Body


def write_json(
    output_path: Path,
    bodies: List[Body],
    frames: List[List[List[float]]],
    params: Dict[str, Any],
    collision_event: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Write simulation results to output_path as JSON.

    Output schema:
    {
        "meta": {
            "dt": ...,
            "total_time": ...,
            "num_frames": ...,
            "collision_event": null | {"frame": N, "body_a": i, "body_b": j, "names": [...]}
        },
        "bodies": [{"name": ..., "mass": ..., "radius_km": ..., "color": ...}, ...],
        "frames": [[[x,y,z], ...], ...]   # frames[t][body_index] = [x, y, z]
    }
    """
    data = {
        "meta": {
            "dt": params["dt"],
            "total_time": params["total_time"],
            "num_frames": len(frames),
            "collision_event": collision_event,
        },
        "bodies": [
            {
                "name": b.name,
                "mass": b.mass,
                "radius_km": b.radius_km,
                "color": b.color,
            }
            for b in bodies
        ],
        "frames": frames,
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f)
