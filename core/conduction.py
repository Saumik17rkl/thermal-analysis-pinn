"""
Heat sink base conduction resistance.

Implements 1D steady-state conduction through the heat sink base
as defined in the Thermal Reference document.
"""

def compute_conduction_resistance(
    base_thickness: float,
    thermal_conductivity: float,
    die_area: float
) -> float:
    """
    Compute conduction resistance through the heat sink base.

    Parameters
    
    base_thickness : float
        Thickness of heat sink base (m)
    thermal_conductivity : float
        Thermal conductivity of heat sink material (W/m·K)
    die_area : float
        Area of processor die (m²)

    Returns
    -------
    float
        Conduction thermal resistance (°C/W)
    """

    if base_thickness <= 0:
        raise ValueError("Base thickness must be positive")
    if thermal_conductivity <= 0:
        raise ValueError("Thermal conductivity must be positive")
    if die_area <= 0:
        raise ValueError("Die area must be positive")

    return base_thickness / (thermal_conductivity * die_area)
