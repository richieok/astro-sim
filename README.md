# astro-sim

A 3D N-body orbital mechanics simulator with an interactive browser-based viewer. Define a system of celestial bodies in JSON, run the simulation, and watch the orbits play back in real time using Three.js.

## Features

- **Leapfrog (velocity-Verlet) integrator** — energy-conserving, suitable for long orbital simulations
- **Collision detection** — halts simulation on first body overlap and reports the event
- **3D interactive viewer** — pan, zoom, and rotate via Three.js OrbitControls
- **Web UI** — paste or load a config, run the simulation, and play back frames without leaving the browser
- **REST API** — `POST /run` accepts a JSON config and returns frame data

## Requirements

- Python 3.8+
- `numpy`
- `flask`

## Installation

```bash
git clone <repo-url>
cd astro-sim
pip install -r requirements.txt
```

## Usage

### Web interface (recommended)

```bash
python sim/server.py
```

Open `http://localhost:8080` in your browser. Paste a config JSON into the editor, click **Run Simulation**, then use the playback controls to step through the animation.

### REST API

Send a `POST` request to `/run` with a JSON body describing the simulation:

```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d @configs/solar_system.json
```

Response:

```json
{
  "num_frames": 8760,
  "collision_event": null
}
```

The viewer at `http://localhost:8080` automatically loads the latest result.

### Python library

```python
from sim.loader import load_config
from sim.simulation import run

bodies, params = load_config("configs/solar_system.json")

for frame in run(bodies, dt=params["dt"], total_time=params["total_time"], every=params["every"]):
    positions = frame["positions"]   # list of [x, y, z] in metres
    if frame["collision"]:
        print("Collision:", frame["collision"])
        break
```

## Configuration format

Configs are JSON files (or dicts) with the following structure:

```json
{
  "dt": 3600,
  "total_time": 31536000,
  "every": 1,
  "bodies": [
    {
      "name": "Sun",
      "mass": 1.989e30,
      "radius_km": 696000,
      "color": "#FFD700",
      "position": [0.0, 0.0, 0.0],
      "velocity": [0.0, 0.0, 0.0]
    },
    {
      "name": "Earth",
      "mass": 5.972e24,
      "radius_km": 6371,
      "color": "#4B9CD3",
      "position": [1.496e11, 0.0, 0.0],
      "velocity": [0.0, 29783.0, 0.0]
    }
  ]
}
```

| Field | Unit | Description |
|---|---|---|
| `dt` | seconds | Time step (default: 3600 — one hour) |
| `total_time` | seconds | Total simulation duration (default: 31536000 — one year) |
| `every` | steps | Record every Nth step to reduce output size |
| `mass` | kg | Body mass |
| `radius_km` | km | Physical radius used for collision detection |
| `position` | metres | Initial position `[x, y, z]` |
| `velocity` | m/s | Initial velocity `[vx, vy, vz]` |

All positions and velocities are in SI units. A positive x-axis points to the right in the viewer; z is up.

## Included configs

| File | Description |
|---|---|
| `configs/solar_system.json` | Sun + Mercury, Venus, Earth, Mars over one year at 1-hour steps |
| `configs/binary_star.json` | Two orbiting stars with a perturbed planet, `every: 24` to thin output |

## Project structure

```
astro-sim/
├── sim/
│   ├── body.py         # Body dataclass
│   ├── integrator.py   # Leapfrog integrator and acceleration computation
│   ├── collision.py    # Pairwise collision detection
│   ├── loader.py       # JSON config parser
│   ├── simulation.py   # run() generator
│   ├── output.py       # Writes viewer/simulation_data.json
│   └── server.py       # Flask server (POST /run, serves viewer/)
├── viewer/
│   └── index.html      # Three.js 3D playback UI
├── configs/
│   ├── solar_system.json
│   └── binary_star.json
└── requirements.txt
```

## Physics notes

- Gravitational constant: `G = 6.674e-11` m³ kg⁻¹ s⁻²
- Acceleration is computed with O(N²) pairwise summation
- The leapfrog integrator conserves energy to ~0.04% over one year at `dt = 3600 s`
- Collision is detected when the distance between two body centres falls below the sum of their radii; the simulation stops at that frame
