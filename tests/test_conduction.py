import pytest
from core.conduction import compute_conduction_resistance


def test_compute_conduction_resistance_valid():
    base_thickness = 0.0025
    k = 167.0
    die_area = 0.0525 * 0.045

    r = compute_conduction_resistance(base_thickness, k, die_area)
    expected = base_thickness / (k * die_area)

    assert pytest.approx(r, rel=1e-6) == expected
    assert r > 0


def test_conduction_resistance_invalid_inputs():
    with pytest.raises(ValueError):
        compute_conduction_resistance(0.0, 167.0, 0.002)

    with pytest.raises(ValueError):
        compute_conduction_resistance(0.0025, -10.0, 0.002)

    with pytest.raises(ValueError):
        compute_conduction_resistance(0.0025, 167.0, 0.0)
