"""
Final thermal solver.

Computes junction temperature using the total
junction-to-ambient thermal resistance.
"""

def compute_junction_temperature(
    ambient_temperature: float,
    heat_dissipation: float,
    total_thermal_resistance: float
) -> float:
    """
    Compute processor junction temperature.

    T_j = T_ambient + Q * R_total

    Parameters
    ----------
    ambient_temperature : float
        Ambient air temperature (°C)
    heat_dissipation : float
        Power dissipated by processor (W)
    total_thermal_resistance : float
        Total junction-to-ambient thermal resistance (°C/W)

    Returns
    -------
    float
        Junction temperature (°C)
    """

    if total_thermal_resistance <= 0:
        raise ValueError("Total thermal resistance must be positive")
    if heat_dissipation < 0:
        raise ValueError("Heat dissipation cannot be negative")

    return ambient_temperature + heat_dissipation * total_thermal_resistance
