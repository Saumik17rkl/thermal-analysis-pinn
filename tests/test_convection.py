"""
Unit tests for forced convection thermal resistance.
"""

import pytest

from core.convection import (
    compute_reynolds_number,
    compute_nusselt_number,
    compute_heat_transfer_coefficient,
    compute_convection_resistance
)


def test_reynolds_number_calculation():
    """
    Test Reynolds number computation.
    """

    velocity = 1.0            # m/s
    fin_spacing = 0.001153    # m
    nu = 1.57e-5              # m²/s

    re = compute_reynolds_number(
        air_velocity=velocity,
        characteristic_length=fin_spacing,
        kinematic_viscosity=nu
    )

    expected = velocity * fin_spacing / nu
    assert pytest.approx(re, rel=1e-6) == expected
    assert re > 0


def test_nusselt_number_laminar():
    """
    Test Nusselt number in laminar regime (Re < 2300).
    """

    re = 500.0
    pr = 0.71
    fin_spacing = 0.001153
    fin_height = 0.0245

    nu = compute_nusselt_number(
        reynolds_number=re,
        prandtl_number=pr,
        fin_spacing=fin_spacing,
        fin_height=fin_height
    )

    assert nu > 0


def test_nusselt_number_turbulent():
    """
    Test Nusselt number in turbulent regime (Re >= 2300).
    """

    re = 5000.0
    pr = 0.71
    fin_spacing = 0.001153
    fin_height = 0.0245

    nu = compute_nusselt_number(
        reynolds_number=re,
        prandtl_number=pr,
        fin_spacing=fin_spacing,
        fin_height=fin_height
    )

    assert nu > 0


def test_heat_transfer_coefficient():
    """
    Test convective heat transfer coefficient computation.
    """

    nu = 10.0
    k_air = 0.0262
    fin_spacing = 0.001153

    h = compute_heat_transfer_coefficient(
        nusselt_number=nu,
        air_thermal_conductivity=k_air,
        fin_spacing=fin_spacing
    )

    expected = nu * k_air / (2 * fin_spacing)
    assert pytest.approx(h, rel=1e-6) == expected
    assert h > 0


def test_convection_resistance_positive():
    """
    Convective resistance should be positive and finite.
    """

    r_conv = compute_convection_resistance(
        air_velocity=1.0,
        fin_spacing=0.001153,
        fin_height=0.0245,
        total_convection_area=0.265,
        air_thermal_conductivity=0.0262,
        kinematic_viscosity=1.57e-5,
        prandtl_number=0.71
    )

    assert r_conv > 0
    assert r_conv < 10.0  # sanity upper bound


def test_convection_resistance_invalid_area():
    """
    Total convection area must be positive.
    """

    with pytest.raises(ValueError):
        compute_convection_resistance(
            air_velocity=1.0,
            fin_spacing=0.001153,
            fin_height=0.0245,
            total_convection_area=0.0,
            air_thermal_conductivity=0.0262,
            kinematic_viscosity=1.57e-5,
            prandtl_number=0.71
        )
