import json
import numpy as np
from typing import Any, Dict, List, Tuple
from .body import Body

# Defaults
DEFAULT_DT = 3600.0          # 1 hour in seconds
DEFAULT_TOTAL_TIME = 31536000.0  # 1 year in seconds
DEFAULT_EVERY = 1            # record every step


def load_config(path: str) -> Tuple[List[Body], Dict[str, Any]]:
    """
    Parse a JSON config file. Returns (bodies, params).

    params keys: dt, total_time, every
    """
    with open(path, "r") as f:
        cfg = json.load(f)

    params = {
        "dt": float(cfg.get("dt", DEFAULT_DT)),
        "total_time": float(cfg.get("total_time", DEFAULT_TOTAL_TIME)),
        "every": int(cfg.get("every", DEFAULT_EVERY)),
    }

    bodies = []
    for entry in cfg["bodies"]:
        radius_km = float(entry["radius_km"])
        radius_m = radius_km * 1000.0
        body = Body(
            name=entry["name"],
            mass=float(entry["mass"]),
            radius=radius_m,
            radius_km=radius_km,
            color=entry.get("color", "#FFFFFF"),
            position=np.array(entry["position"], dtype=float),
            velocity=np.array(entry["velocity"], dtype=float),
        )
        bodies.append(body)

    return bodies, params


def load_config_dict(cfg: Dict[str, Any]) -> Tuple[List[Body], Dict[str, Any]]:
    """Parse a config dict (e.g. from Flask JSON body). Returns (bodies, params)."""
    params = {
        "dt": float(cfg.get("dt", DEFAULT_DT)),
        "total_time": float(cfg.get("total_time", DEFAULT_TOTAL_TIME)),
        "every": int(cfg.get("every", DEFAULT_EVERY)),
    }

    bodies = []
    for entry in cfg["bodies"]:
        radius_km = float(entry["radius_km"])
        radius_m = radius_km * 1000.0
        body = Body(
            name=entry["name"],
            mass=float(entry["mass"]),
            radius=radius_m,
            radius_km=radius_km,
            color=entry.get("color", "#FFFFFF"),
            position=np.array(entry["position"], dtype=float),
            velocity=np.array(entry["velocity"], dtype=float),
        )
        bodies.append(body)

    return bodies, params
