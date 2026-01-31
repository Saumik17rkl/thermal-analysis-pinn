"""
Forced convection thermal resistance for heat sink fins.

Implements channel flow convection between parallel plates
as defined in the Thermal Reference document.
"""

import math

def compute_reynolds_number(
    air_velocity: float,
    characteristic_length: float,
    kinematic_viscosity: float
) -> float:
    """
    Compute Reynolds number.

    Re = V * L / nu
    """
    if air_velocity <= 0:
        raise ValueError("Air velocity must be positive")
    if characteristic_length <= 0:
        raise ValueError("Characteristic length must be positive")
    if kinematic_viscosity <= 0:
        raise ValueError("Kinematic viscosity must be positive")

    return air_velocity * characteristic_length / kinematic_viscosity


def compute_nusselt_number(
    reynolds_number: float,
    prandtl_number: float,
    fin_spacing: float,
    fin_height: float
) -> float:
    """
    Compute Nusselt number based on flow regime.

    - Laminar (Re < 2300): Sieder-Tate correlation
    - Turbulent (Re >= 2300): Dittus-Boelter correlation
    """

    if reynolds_number <= 0:
        raise ValueError("Reynolds number must be positive")
    if prandtl_number <= 0:
        raise ValueError("Prandtl number must be positive")
    if fin_spacing <= 0:
        raise ValueError("Fin spacing must be positive")
    if fin_height <= 0:
        raise ValueError("Fin height must be positive")

    # Laminar flow
    if reynolds_number < 2300:
        return 1.86 * (
            reynolds_number
            * prandtl_number
            * (2 * fin_spacing / fin_height)
        ) ** (1.0 / 3.0)

    # Turbulent flow
    return 0.023 * (reynolds_number ** 0.8) * (prandtl_number ** 0.3)


def compute_heat_transfer_coefficient(
    nusselt_number: float,
    air_thermal_conductivity: float,
    fin_spacing: float
) -> float:
    """
    Compute convective heat transfer coefficient.

    h = Nu * k_air / (2 * fin_spacing)
    """

    if nusselt_number <= 0:
        raise ValueError("Nusselt number must be positive")
    if air_thermal_conductivity <= 0:
        raise ValueError("Air thermal conductivity must be positive")
    if fin_spacing <= 0:
        raise ValueError("Fin spacing must be positive")

    return nusselt_number * air_thermal_conductivity / (2 * fin_spacing)


def compute_fin_efficiency(
    fin_height: float,
    heat_transfer_coefficient: float,
    fin_thickness: float,
    thermal_conductivity: float = 167.0
) -> float:
    """
    Compute fin efficiency for rectangular fins.
    
    η_fin = tanh(m*L) / (m*L)
    where m = sqrt(2*h/(k*t))
    """
    
    if fin_height <= 0:
        raise ValueError("Fin height must be positive")
    if heat_transfer_coefficient <= 0:
        raise ValueError("Heat transfer coefficient must be positive")
    if fin_thickness <= 0:
        raise ValueError("Fin thickness must be positive")
    if thermal_conductivity <= 0:
        raise ValueError("Thermal conductivity must be positive")
    
    m = (2.0 * heat_transfer_coefficient / (thermal_conductivity * fin_thickness)) ** 0.5
    m_l = m * fin_height
    
    if m_l > 10:  # Prevent overflow for very long fins
        return 1.0 / (m_l)
    
    return math.tanh(m_l) / m_l


def compute_convection_resistance(
    air_velocity: float,
    fin_spacing: float,
    fin_height: float,
    total_convection_area: float,
    air_thermal_conductivity: float,
    kinematic_viscosity: float,
    prandtl_number: float,
    fin_thickness: float = 0.0008,
    sink_thermal_conductivity: float = 167.0
) -> float:
    """
    Compute convective thermal resistance of the heat sink.

    R_conv = 1 / (h * A_total * η_fin)
    """

    if total_convection_area <= 0:
        raise ValueError("Total convection area must be positive")

    reynolds_number = compute_reynolds_number(
        air_velocity=air_velocity,
        characteristic_length=fin_spacing,
        kinematic_viscosity=kinematic_viscosity
    )

    nusselt_number = compute_nusselt_number(
        reynolds_number=reynolds_number,
        prandtl_number=prandtl_number,
        fin_spacing=fin_spacing,
        fin_height=fin_height
    )

    h = compute_heat_transfer_coefficient(
        nusselt_number=nusselt_number,
        air_thermal_conductivity=air_thermal_conductivity,
        fin_spacing=fin_spacing
    )

    fin_efficiency = compute_fin_efficiency(
        fin_height=fin_height,
        heat_transfer_coefficient=h,
        fin_thickness=fin_thickness,
        thermal_conductivity=sink_thermal_conductivity
    )

    return 1.0 / (h * total_convection_area * fin_efficiency)
