"""
Thermal analysis service layer.

This module orchestrates the validated core thermal physics
and prepares results for API responses.
"""

from core.geometry import (
    compute_die_area,
    compute_fin_spacing,
    compute_total_convection_area
)
from core.tim import compute_tim_resistance
from core.conduction import compute_conduction_resistance
from core.convection import compute_convection_resistance
from core.resistance_network import (
    compute_heat_sink_resistance,
    compute_total_resistance
)
from core.solver import compute_junction_temperature

from ..schemas import (
    ThermalRequestSchema,
    ThermalResponseSchema
)


def run_thermal_analysis(payload: dict) -> dict:
    """
    Run full thermal analysis using the validated physics model.

    Parameters
    ----------
    payload : dict
        Input JSON payload from API request

    Returns
    -------
    dict
        Structured thermal analysis results
    """

    # -----------------------------
    # Validate request structure
    # -----------------------------
    data = ThermalRequestSchema.validate(payload)

    # -----------------------------
    # Extract inputs
    # -----------------------------
    processor = data["processor"]
    heat_sink = data["heat_sink"]
    tim = data["tim"]
    air = data["air"]
    ambient = data["ambient"]

    # -----------------------------
    # Geometry calculations
    # -----------------------------
    die_area = compute_die_area(
        processor["die_length"],
        processor["die_width"]
    )

    fin_spacing = compute_fin_spacing(
        heat_sink["sink_width"],
        heat_sink["number_of_fins"],
        heat_sink["fin_thickness"]
    )

    convection_area = compute_total_convection_area(
        heat_sink["fin_height"],
        heat_sink["sink_length"],
        heat_sink["number_of_fins"]
    )

    # -----------------------------
    # Individual resistances
    # -----------------------------
    r_tim = compute_tim_resistance(
        tim["thickness"],
        tim["thermal_conductivity"],
        die_area
    )

    r_conduction = compute_conduction_resistance(
        heat_sink["base_thickness"],
        data["heat_sink"].get("thermal_conductivity", 167.0),
        die_area
    )

    r_convection = compute_convection_resistance(
        air_velocity=air["velocity"],
        fin_spacing=fin_spacing,
        fin_height=heat_sink["fin_height"],
        total_convection_area=convection_area,
        air_thermal_conductivity=air["thermal_conductivity"],
        kinematic_viscosity=air["kinematic_viscosity"],
        prandtl_number=air["prandtl_number"],
        fin_thickness=heat_sink["fin_thickness"],
        sink_thermal_conductivity=data["heat_sink"].get("thermal_conductivity", 167.0)
    )

    # -----------------------------
    # Resistance network
    # -----------------------------
    r_heat_sink = compute_heat_sink_resistance(
        r_conduction,
        r_convection
    )

    r_total = compute_total_resistance(
        data["junction_to_case_resistance"],
        r_tim,
        r_heat_sink
    )

    # -----------------------------
    # Final junction temperature
    # -----------------------------
    junction_temperature = compute_junction_temperature(
        ambient_temperature=ambient["temperature"],
        heat_dissipation=processor["power"],
        total_thermal_resistance=r_total
    )

    # -----------------------------
    # Build response
    # -----------------------------
    return ThermalResponseSchema.build(
        r_tim=r_tim,
        r_conduction=r_conduction,
        r_convection=r_convection,
        r_heat_sink=r_heat_sink,
        r_total=r_total,
        junction_temperature=junction_temperature
    )
