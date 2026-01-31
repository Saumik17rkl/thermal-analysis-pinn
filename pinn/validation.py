"""
Physics-based validation utilities for the thermal PINN.

Checks:
1. Energy conservation
2. Consistency with lumped thermal model
3. Physical temperature monotonicity
"""

import numpy as np
import torch


# 1. Energy balance check

def check_energy_balance(
    model: torch.nn.Module,
    surface_points: np.ndarray,
    heat_transfer_coefficient: float,
    ambient_temperature: float,
    expected_power: float,
    tolerance: float = 0.1
) -> bool:
    """
    Validate that total convective heat removal ≈ input power.

    ∫ h (T - T_ambient) dA ≈ Q

    Parameters
    ----------
    model : torch.nn.Module
        Trained PINN model
    surface_points : np.ndarray
        Convective surface points (N, 3)
    heat_transfer_coefficient : float
        Convective heat transfer coefficient (W/m²K)
    ambient_temperature : float
        Ambient temperature (°C)
    expected_power : float
        Input heat power (W)
    tolerance : float
        Relative tolerance (fraction)

    Returns
    -------
    bool
        True if energy balance is satisfied
    """

    model.eval()
    with torch.no_grad():
        pts = torch.tensor(surface_points, dtype=torch.float32)
        temperatures = model(pts).cpu().numpy().flatten()

    heat_flux = heat_transfer_coefficient * (temperatures - ambient_temperature)
    estimated_power = np.mean(heat_flux)

    relative_error = abs(estimated_power - expected_power) / expected_power
    return relative_error <= tolerance


# 2. Lumped-model consistency check

def check_lumped_model_consistency(
    model: torch.nn.Module,
    base_points: np.ndarray,
    expected_base_temperature: float,
    tolerance: float = 2.0
) -> bool:
    """
    Check that mean base temperature matches lumped model.

    Parameters
    ----------
    model : torch.nn.Module
        Trained PINN model
    base_points : np.ndarray
        Points on base surface (N, 3)
    expected_base_temperature : float
        Base temperature from lumped model (°C)
    tolerance : float
        Absolute tolerance (°C)

    Returns
    -------
    bool
        True if consistency condition is met
    """

    model.eval()
    with torch.no_grad():
        pts = torch.tensor(base_points, dtype=torch.float32)
        temperatures = model(pts).cpu().numpy().flatten()

    mean_base_temperature = np.mean(temperatures)
    return abs(mean_base_temperature - expected_base_temperature) <= tolerance


# 3. Physical monotonicity check

def check_temperature_monotonicity(
    model: torch.nn.Module,
    base_points: np.ndarray,
    top_points: np.ndarray
) -> bool:
    """
    Ensure temperature decreases from base to fin tip.

    T_base > T_top

    Returns
    -------
    bool
        True if monotonicity condition holds
    """

    model.eval()
    with torch.no_grad():
        base_temps = model(
            torch.tensor(base_points, dtype=torch.float32)
        ).cpu().numpy().flatten()

        top_temps = model(
            torch.tensor(top_points, dtype=torch.float32)
        ).cpu().numpy().flatten()

    return np.mean(base_temps) > np.mean(top_temps)
