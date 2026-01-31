"""
Unit tests for geometric calculations.
"""

import pytest

from core.geometry import (
    compute_die_area,
    compute_fin_spacing,
    compute_total_convection_area
)


def test_compute_die_area():
    """
    Test die area calculation.
    """

    die_length = 0.0525  # m
    die_width = 0.045   # m

    area = compute_die_area(die_length, die_width)
    expected = die_length * die_width

    assert pytest.approx(area, rel=1e-6) == expected
    assert area > 0


def test_compute_fin_spacing():
    """
    Test fin spacing calculation.
    """

    sink_width = 0.116
    number_of_fins = 60
    fin_thickness = 0.0008

    spacing = compute_fin_spacing(
        sink_width,
        number_of_fins,
        fin_thickness
    )

    expected = (sink_width - number_of_fins * fin_thickness) / (number_of_fins - 1)

    assert pytest.approx(spacing, rel=1e-6) == expected
    assert spacing > 0


def test_compute_total_convection_area():
    """
    Test total convection area calculation.
    """

    fin_height = 0.0245
    sink_length = 0.09
    number_of_fins = 60

    area = compute_total_convection_area(
        fin_height,
        sink_length,
        number_of_fins
    )

    expected = 2.0 * number_of_fins * fin_height * sink_length

    assert pytest.approx(area, rel=1e-6) == expected
    assert area > 0


def test_fin_spacing_invalid_geometry():
    """
    Fin spacing should fail if fins occupy entire sink width.
    """

    with pytest.raises(ValueError):
        compute_fin_spacing(
            sink_width=0.05,
            number_of_fins=100,
            fin_thickness=0.001
        )


def test_negative_dimensions():
    """
    Geometry dimensions must be positive.
    """

    with pytest.raises(ValueError):
        compute_die_area(-0.05, 0.04)

    with pytest.raises(ValueError):
        compute_total_convection_area(0.02, -0.1, 50)
