"""
Geometric calculations for the thermal model.

This module computes derived geometric quantities such as
die area, fin spacing, and total convection area.
"""

def compute_die_area(
    die_length: float,
    die_width: float
) -> float:
    """
    Compute processor die area.

    Parameters
    ----------
    die_length : float
        Die length (m)
    die_width : float
        Die width (m)

    Returns
    -------
    float
        Die area (m²)
    """

    if die_length <= 0:
        raise ValueError("Die length must be positive")
    if die_width <= 0:
        raise ValueError("Die width must be positive")

    return die_length * die_width


def compute_fin_spacing(
    sink_width: float,
    number_of_fins: int,
    fin_thickness: float
) -> float:
    """
    Compute spacing between adjacent fins.

    Formula (from reference):
    Sf = (sink_width - N_fins * fin_thickness) / (N_fins - 1)

    Parameters
    ----------
    sink_width : float
        Total heat sink width (m)
    number_of_fins : int
        Number of fins
    fin_thickness : float
        Thickness of a single fin (m)

    Returns
    -------
    float
        Fin spacing (m)
    """

    if sink_width <= 0:
        raise ValueError("Sink width must be positive")
    if number_of_fins <= 1:
        raise ValueError("Number of fins must be greater than 1")
    if fin_thickness <= 0:
        raise ValueError("Fin thickness must be positive")

    usable_width = sink_width - number_of_fins * fin_thickness
    if usable_width <= 0:
        raise ValueError("Invalid fin geometry: fins occupy entire sink width")

    return usable_width / (number_of_fins - 1)


def compute_total_convection_area(
    fin_height: float,
    sink_length: float,
    number_of_fins: int
) -> float:
    """
    Compute total convection surface area of the fins.

    Assumes convection occurs on both sides of each fin.

    A_total = 2 * N_fins * fin_height * sink_length

    Parameters
    ----------
    fin_height : float
        Height of a fin (m)
    sink_length : float
        Length of heat sink (m)
    number_of_fins : int
        Number of fins

    Returns
    -------
    float
        Total convection area (m²)
    """

    if fin_height <= 0:
        raise ValueError("Fin height must be positive")
    if sink_length <= 0:
        raise ValueError("Sink length must be positive")
    if number_of_fins <= 0:
        raise ValueError("Number of fins must be positive")

    return 2.0 * number_of_fins * fin_height * sink_length
