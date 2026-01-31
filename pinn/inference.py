"""
PINN inference utilities.

Provides functions to evaluate a trained PINN model
and predict temperature at given spatial locations.
"""

import torch
import numpy as np


def predict_temperature(
    model: torch.nn.Module,
    points: np.ndarray,
    device: str = "cpu"
) -> np.ndarray:
    """
    Predict temperature at given spatial points using a trained PINN.

    Parameters
    ----------
    model : torch.nn.Module
        Trained PINN model
    points : np.ndarray
        Array of shape (N, 3) containing (x, y, z) coordinates
    device : str
        Device to run inference on ("cpu" or "cuda")

    Returns
    -------
    np.ndarray
        Predicted temperatures of shape (N,)
    """

    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("Points array must have shape (N, 3)")

    model.eval()
    model.to(device)

    with torch.no_grad():
        inputs = torch.tensor(points, dtype=torch.float32, device=device)
        temperatures = model(inputs)

    return temperatures.cpu().numpy().flatten()


def predict_temperature_field(
    model: torch.nn.Module,
    domain,
    n_points: int = 1000,
    device: str = "cpu"
) -> np.ndarray:
    """
    Predict temperature field inside the heat sink volume.

    Samples interior points from the domain and predicts temperature.

    Parameters
    ----------
    model : torch.nn.Module
        Trained PINN model
    domain : HeatSinkDomain
        Spatial domain object
    n_points : int
        Number of interior sample points
    device : str
        Device to run inference on

    Returns
    -------
    np.ndarray
        Array of shape (N, 4): (x, y, z, T)
    """

    if n_points <= 0:
        raise ValueError("Number of points must be positive")

    points = domain.sample_interior(n_points)
    temperatures = predict_temperature(
        model=model,
        points=points,
        device=device
    )

    return np.column_stack((points, temperatures))
