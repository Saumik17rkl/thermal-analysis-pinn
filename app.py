from flask import Flask, request, jsonify
import torch
import numpy as np

from model_def import PINN

# -----------------------------
# App setup
# -----------------------------
app = Flask(__name__)

DEFAULT_AMBIENT = 25.0

# -----------------------------
# Load trained model
# -----------------------------
model = PINN()
model.load_state_dict(torch.load("model/thermal_pinn_model.pth", map_location="cpu"))
model.eval()


# -----------------------------
# Input validation
# -----------------------------
def validate_payload(data):
    required_fields = ["power", "fin_height", "air_velocity"]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing field: {field}")

    power = float(data["power"])
    fin_height = float(data["fin_height"])
    air_velocity = float(data["air_velocity"])
    ambient = float(data.get("ambient_temp", DEFAULT_AMBIENT))

    if power <= 0:
        raise ValueError("Power must be > 0")
    if fin_height <= 0:
        raise ValueError("Fin height must be > 0")
    if air_velocity <= 0:
        raise ValueError("Air velocity must be > 0")

    return power, fin_height, air_velocity, ambient


# -----------------------------
# API route
# -----------------------------
@app.route("/thermal/predict", methods=["POST"])
def predict_temperature():
    try:
        data = request.get_json(force=True)

        power, fin_height, air_velocity, ambient = validate_payload(data)

        x = torch.tensor(
            [[power, fin_height, air_velocity]],
            dtype=torch.float32
        )

        with torch.no_grad():
            delta_T = model(x).item()

        Tj = ambient + delta_T

        return jsonify({
            "inputs": {
                "power": power,
                "fin_height": fin_height,
                "air_velocity": air_velocity,
                "ambient_temp": ambient
            },
            "results": {
                "temperature_rise": round(delta_T, 2),
                "junction_temperature": round(Tj, 2)
            }
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
