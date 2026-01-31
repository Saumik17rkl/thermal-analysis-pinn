"""
Thermal Interface Material (TIM) resistance calculation.

Implements thermal resistance due to the TIM layer
between processor die and heat sink base.
"""

def compute_tim_resistance(
    tim_thickness: float,
    tim_thermal_conductivity: float,
    die_area: float
) -> float:
    """
    Compute thermal resistance of the TIM layer.

    R_TIM = t_TIM / (k_TIM * A_die)

    Parameters
    ----------
    tim_thickness : float
        Thickness of TIM layer (m)
    tim_thermal_conductivity : float
        Thermal conductivity of TIM (W/m·K)
    die_area : float
        Area of processor die (m²)

    Returns
    -------
    float
        TIM thermal resistance (°C/W)
    """

    if tim_thickness <= 0:
        raise ValueError("TIM thickness must be positive")
    if tim_thermal_conductivity <= 0:
        raise ValueError("TIM thermal conductivity must be positive")
    if die_area <= 0:
        raise ValueError("Die area must be positive")

    return tim_thickness / (tim_thermal_conductivity * die_area)
