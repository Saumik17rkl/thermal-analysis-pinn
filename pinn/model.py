"""
Neural network architecture for the thermal PINN.

Maps spatial coordinates (x, y, z) to temperature T.
"""

import torch
import torch.nn as nn


class ThermalPINN(nn.Module):
    """
    Fully-connected neural network for temperature prediction.

    Input:
        (x, y, z)

    Output:
        T (temperature)
    """

    def __init__(
        self,
        input_dim: int = 3,
        hidden_dim: int = 64,
        num_hidden_layers: int = 4
    ):
        super().__init__()

        if num_hidden_layers < 1:
            raise ValueError("Number of hidden layers must be >= 1")

        layers = []

        # Input layer
        layers.append(nn.Linear(input_dim, hidden_dim))
        layers.append(nn.Tanh())

        # Hidden layers
        for _ in range(num_hidden_layers - 1):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            layers.append(nn.Tanh())

        # Output layer
        layers.append(nn.Linear(hidden_dim, 1))

        self.network = nn.Sequential(*layers)

        self._initialize_weights()

    def _initialize_weights(self):
        """
        Xavier initialization for stable PINN training.
        """
        for m in self.network:
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.

        Parameters
        ----------
        x : torch.Tensor
            Tensor of shape (N, 3)

        Returns
        -------
        torch.Tensor
            Temperature predictions of shape (N, 1)
        """

        if x.ndim != 2 or x.shape[1] != 3:
            raise ValueError("Input tensor must have shape (N, 3)")

        return self.network(x)
