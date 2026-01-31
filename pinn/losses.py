"""
Physics-informed loss functions for thermal PINN.

Implements:
- PDE residual loss (steady-state heat equation)
- Boundary condition losses
- Consistency loss with lumped thermal model
"""

import torch


# PDE: Steady-state heat equation

def pde_residual_loss(
    model: torch.nn.Module,
    points: torch.Tensor,
    thermal_conductivity: float
) -> torch.Tensor:
    """
    Enforce steady-state heat equation:
        ∇ · (k ∇T) = 0

    Parameters
    ----------
    model : torch.nn.Module
        PINN model
    points : torch.Tensor
        Interior collocation points (N, 3)
    thermal_conductivity : float
        Thermal conductivity (W/m·K)

    Returns
    -------
    torch.Tensor
        Mean squared PDE residual
    """

    points.requires_grad_(True)
    temperature = model(points)

    grads = torch.autograd.grad(
        outputs=temperature,
        inputs=points,
        grad_outputs=torch.ones_like(temperature),
        create_graph=True
    )[0]

    dT_dx = grads[:, 0]
    dT_dy = grads[:, 1]
    dT_dz = grads[:, 2]

    d2T_dx2 = torch.autograd.grad(
        dT_dx, points, grad_outputs=torch.ones_like(dT_dx), create_graph=True
    )[0][:, 0]

    d2T_dy2 = torch.autograd.grad(
        dT_dy, points, grad_outputs=torch.ones_like(dT_dy), create_graph=True
    )[0][:, 1]

    d2T_dz2 = torch.autograd.grad(
        dT_dz, points, grad_outputs=torch.ones_like(dT_dz), create_graph=True
    )[0][:, 2]

    laplacian = d2T_dx2 + d2T_dy2 + d2T_dz2

    residual = thermal_conductivity * laplacian
    return torch.mean(residual ** 2)


# Boundary condition: Base heat flux

def base_heat_flux_loss(
    model: torch.nn.Module,
    base_points: torch.Tensor,
    heat_flux: float,
    thermal_conductivity: float
) -> torch.Tensor:
    """
    Enforce heat flux at the die–base interface:
        -k * dT/dn = q''

    Assumes normal direction is +z.
    """

    base_points.requires_grad_(True)
    temperature = model(base_points)

    grads = torch.autograd.grad(
        outputs=temperature,
        inputs=base_points,
        grad_outputs=torch.ones_like(temperature),
        create_graph=True
    )[0]

    dT_dz = grads[:, 2]
    flux_residual = -thermal_conductivity * dT_dz - heat_flux

    return torch.mean(flux_residual ** 2)


# Boundary condition: Convective surfaces

def convection_boundary_loss(
    model: torch.nn.Module,
    surface_points: torch.Tensor,
    heat_transfer_coefficient: float,
    ambient_temperature: float,
    thermal_conductivity: float
) -> torch.Tensor:
    """
    Enforce convective boundary condition:
        -k * dT/dn = h (T - T_ambient)

    Assumes outward normal is +z.
    """

    surface_points.requires_grad_(True)
    temperature = model(surface_points)

    grads = torch.autograd.grad(
        outputs=temperature,
        inputs=surface_points,
        grad_outputs=torch.ones_like(temperature),
        create_graph=True
    )[0]

    dT_dz = grads[:, 2]
    convective_residual = (
        -thermal_conductivity * dT_dz
        - heat_transfer_coefficient * (temperature.squeeze() - ambient_temperature)
    )

    return torch.mean(convective_residual ** 2)


# Consistency with lumped thermal model

def lumped_model_consistency_loss(
    model: torch.nn.Module,
    base_points: torch.Tensor,
    expected_base_temperature: float
) -> torch.Tensor:
    """
    Enforce consistency with lumped thermal model:
        mean(T_base_PINN) ≈ T_base_lumped
    """

    temperature = model(base_points).squeeze()
    return torch.mean((temperature - expected_base_temperature) ** 2)
