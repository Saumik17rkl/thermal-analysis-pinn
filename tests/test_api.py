"""
End-to-end API tests for the thermal analysis service.
"""

import json
import pytest

from app.main import create_app


@pytest.fixture
def client():
    """
    Create a Flask test client.
    """
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_thermal_solve_endpoint_success(client):
    """
    Test /thermal/solve endpoint with valid reference inputs.
    """

    payload = {
        "processor": {
            "die_length": 0.0525,
            "die_width": 0.045,
            "power": 150.0
        },
        "heat_sink": {
            "sink_length": 0.09,
            "sink_width": 0.116,
            "base_thickness": 0.0025,
            "number_of_fins": 60,
            "fin_thickness": 0.0008,
            "fin_height": 0.0245
        },
        "tim": {
            "thermal_conductivity": 4.0,
            "thickness": 0.0001
        },
        "air": {
            "velocity": 1.0,
            "thermal_conductivity": 0.0262,
            "kinematic_viscosity": 1.57e-5,
            "prandtl_number": 0.71
        },
        "ambient": {
            "temperature": 25.0
        },
        "junction_to_case_resistance": 0.1
    }

    response = client.post(
        "/thermal/solve",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 200

    data = response.get_json()

    # Response structure checks
    assert "resistances" in data
    assert "junction_temperature" in data

    resistances = data["resistances"]

    for key in ["tim", "conduction", "convection", "heat_sink", "total"]:
        assert key in resistances
        assert resistances[key] > 0

    # Physical sanity checks
    assert data["junction_temperature"] > payload["ambient"]["temperature"]

    # Expected ballpark values (from current physics model)
    assert 0.1 < resistances["heat_sink"] < 0.15
    assert 55.0 < data["junction_temperature"] < 65.0


def test_thermal_solve_missing_payload(client):
    """
    Test API behavior when request body is missing.
    """

    response = client.post("/thermal/solve")
    assert response.status_code == 400


def test_thermal_solve_invalid_json(client):
    """
    Test API behavior with invalid JSON input.
    """

    response = client.post(
        "/thermal/solve",
        data="not a json",
        content_type="application/json"
    )

    assert response.status_code == 400
