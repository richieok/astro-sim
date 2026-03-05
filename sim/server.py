import json
import sys
from pathlib import Path

# Ensure project root is on path when running as a script
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, jsonify, request, send_from_directory

try:
    from .loader import load_config_dict
    from .simulation import run as run_sim
    from .output import write_json
except ImportError:
    from sim.loader import load_config_dict
    from sim.simulation import run as run_sim
    from sim.output import write_json

VIEWER_DIR = PROJECT_ROOT / "viewer"
CONFIGS_DIR = PROJECT_ROOT / "configs"
OUTPUT_PATH = VIEWER_DIR / "simulation_data.json"

app = Flask(__name__, static_folder=str(VIEWER_DIR))


@app.route("/")
def index():
    return send_from_directory(VIEWER_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(VIEWER_DIR, filename)


@app.route("/presets", methods=["GET"])
def get_presets():
    presets = {}
    for path in CONFIGS_DIR.glob("*.json"):
        key = path.stem
        with open(path) as f:
            presets[key] = json.load(f)
    return jsonify(presets)


@app.route("/run", methods=["POST"])
def run_simulation():
    cfg = request.get_json(force=True)
    if not cfg:
        return jsonify({"error": "No JSON body provided"}), 400

    try:
        bodies, params = load_config_dict(cfg)
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid config: {e}"}), 400

    frames = []
    collision_event = None

    for frame_data in run_sim(
        bodies,
        dt=params["dt"],
        total_time=params["total_time"],
        every=params["every"],
    ):
        frames.append(frame_data["positions"])
        if frame_data["collision"] is not None:
            collision_event = frame_data["collision"]
            break

    write_json(OUTPUT_PATH, bodies, frames, params, collision_event)

    return jsonify({
        "num_frames": len(frames),
        "collision_event": collision_event,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
