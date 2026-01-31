"""
Thermal resistance network assembly.

Combines individual thermal resistances into
heat sink resistance and total junction-to-ambient resistance.
"""

def compute_heat_sink_resistance(
    conduction_resistance: float,
    convection_resistance: float
) -> float:
    """
    Compute total heat sink thermal resistance.

    R_hs = R_cond + R_conv
    """

    if conduction_resistance <= 0:
        raise ValueError("Conduction resistance must be positive")
    if convection_resistance <= 0:
        raise ValueError("Convection resistance must be positive")

    return conduction_resistance + convection_resistance


def compute_total_resistance(
    junction_to_case_resistance: float,
    tim_resistance: float,
    heat_sink_resistance: float
) -> float:
    """
    Compute total thermal resistance from junction to ambient.

    R_total = R_jc + R_TIM + R_hs
    """

    if junction_to_case_resistance < 0:
        raise ValueError("Junction-to-case resistance cannot be negative")
    if tim_resistance <= 0:
        raise ValueError("TIM resistance must be positive")
    if heat_sink_resistance <= 0:
        raise ValueError("Heat sink resistance must be positive")

    return (
        junction_to_case_resistance
        + tim_resistance
        + heat_sink_resistance
    )
