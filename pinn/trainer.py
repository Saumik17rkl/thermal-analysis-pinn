"""
Training loop for the thermal Physics-Informed Neural Network (PINN).

This module:
- Samples domain and boundary points
- Computes physics-informed losses
- Optimizes the neural network parameters
"""

import torch
import torch.optim as optim

from pinn.losses import (
    pde_residual_loss,
    base_heat_flux_loss,
    convection_boundary_loss,
    lumped_model_consistency_loss
)


class PINNTrainer:
    """
    Trainer for the thermal PINN.
    """

    def __init__(
        self,
        model: torch.nn.Module,
        domain,
        thermal_conductivity: float,
        heat_flux: float,
        heat_transfer_coefficient: float,
        ambient_temperature: float,
        expected_base_temperature: float,
        device: str = "cpu"
    ):
        self.model = model.to(device)
        self.domain = domain
        self.k = thermal_conductivity
        self.q_flux = heat_flux
        self.h = heat_transfer_coefficient
        self.T_ambient = ambient_temperature
        self.T_base_expected = expected_base_temperature
        self.device = device

    def train(
        self,
        epochs: int = 5000,
        lr: float = 1e-3,
        n_interior: int = 2000,
        n_base: int = 500,
        n_surface: int = 500,
        loss_weights: dict | None = None
    ):
        """
        Train the PINN.

        Parameters
        ----------
        epochs : int
            Number of training epochs
        lr : float
            Learning rate
        n_interior : int
            Number of interior collocation points
        n_base : int
            Number of base boundary points
        n_surface : int
            Number of convective surface points
        loss_weights : dict
            Optional weights for loss components
        """

        if loss_weights is None:
            loss_weights = {
                "pde": 1.0,
                "base": 1.0,
                "conv": 1.0,
                "lumped": 0.5
            }

        optimizer = optim.Adam(self.model.parameters(), lr=lr)

        for epoch in range(1, epochs + 1):

            
            # Sample domain points
            interior_pts = torch.tensor(
                self.domain.sample_interior(n_interior),
                dtype=torch.float32,
                device=self.device
            )

            base_pts = torch.tensor(
                self.domain.sample_base(n_base),
                dtype=torch.float32,
                device=self.device
            )

            surface_pts = torch.tensor(
                self.domain.sample_top(n_surface),
                dtype=torch.float32,
                device=self.device
            )

            loss_pde = pde_residual_loss(
                self.model, interior_pts, self.k
            )

            loss_base = base_heat_flux_loss(
                self.model, base_pts, self.q_flux, self.k
            )

            loss_conv = convection_boundary_loss(
                self.model,
                surface_pts,
                self.h,
                self.T_ambient,
                self.k
            )

            loss_lumped = lumped_model_consistency_loss(
                self.model,
                base_pts,
                self.T_base_expected
            )

            total_loss = (
                loss_weights["pde"] * loss_pde
                + loss_weights["base"] * loss_base
                + loss_weights["conv"] * loss_conv
                + loss_weights["lumped"] * loss_lumped
            )

            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()

            if epoch % 500 == 0 or epoch == 1:
                print(
                    f"[Epoch {epoch:5d}] "
                    f"Total={total_loss.item():.4e} | "
                    f"PDE={loss_pde.item():.2e} | "
                    f"Base={loss_base.item():.2e} | "
                    f"Conv={loss_conv.item():.2e} | "
                    f"Lumped={loss_lumped.item():.2e}"
                )

    def save_model(self, path: str):
        """
        Save trained PINN model weights.
        """
        torch.save(self.model.state_dict(), path)
