"""
Thermal analysis API routes.

Defines REST endpoints for computing thermal resistances
and junction temperature using the validated core model.
"""

from flask import Blueprint, request, jsonify

from ..services.thermal_service import run_thermal_analysis

thermal_bp = Blueprint("thermal", __name__, url_prefix="/thermal")


@thermal_bp.route("/solve", methods=["POST"])
def solve_thermal():
    """
    Solve thermal model for given inputs.

    Expects JSON payload containing:
    - processor parameters
    - heat sink geometry
    - TIM properties
    - air properties
    - ambient temperature

    Returns:
    - Individual resistances
    - Total resistance
    - Junction temperature
    """

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    payload = request.get_json()

    try:
        results = run_thermal_analysis(payload)
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Catch-all to avoid leaking stack traces
        return jsonify({"error": "Internal server error"}), 500

    return jsonify(results), 200
