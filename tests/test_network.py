"""
Unit tests for thermal resistance network assembly.
"""

import pytest

from core.resistance_network import (
    compute_heat_sink_resistance,
    compute_total_resistance
)


def test_compute_heat_sink_resistance():
    """
    Heat sink resistance should be sum of conduction and convection.
    """

    r_cond = 0.05
    r_conv = 0.32

    r_hs = compute_heat_sink_resistance(
        conduction_resistance=r_cond,
        convection_resistance=r_conv
    )

    expected = r_cond + r_conv

    assert pytest.approx(r_hs, rel=1e-6) == expected
    assert r_hs > 0


def test_compute_total_resistance():
    """
    Total resistance should be sum of Rjc, RTIM, and Rhs.
    """

    r_jc = 0.1
    r_tim = 0.02
    r_hs = 0.35

    r_total = compute_total_resistance(
        junction_to_case_resistance=r_jc,
        tim_resistance=r_tim,
        heat_sink_resistance=r_hs
    )

    expected = r_jc + r_tim + r_hs

    assert pytest.approx(r_total, rel=1e-6) == expected
    assert r_total > 0


def test_heat_sink_resistance_invalid_inputs():
    """
    Heat sink resistance inputs must be positive.
    """

    with pytest.raises(ValueError):
        compute_heat_sink_resistance(
            conduction_resistance=0.0,
            convection_resistance=0.3
        )

    with pytest.raises(ValueError):
        compute_heat_sink_resistance(
            conduction_resistance=0.1,
            convection_resistance=-0.2
        )


def test_total_resistance_invalid_inputs():
    """
    Total resistance inputs must be physically valid.
    """

    with pytest.raises(ValueError):
        compute_total_resistance(
            junction_to_case_resistance=-0.1,
            tim_resistance=0.02,
            heat_sink_resistance=0.3
        )

    with pytest.raises(ValueError):
        compute_total_resistance(
            junction_to_case_resistance=0.1,
            tim_resistance=0.0,
            heat_sink_resistance=0.3
        )

    with pytest.raises(ValueError):
        compute_total_resistance(
            junction_to_case_resistance=0.1,
            tim_resistance=0.02,
            heat_sink_resistance=0.0
        )
