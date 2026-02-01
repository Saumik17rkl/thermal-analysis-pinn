import torch
import torch.nn as nn


class PINN(nn.Module):
    def __init__(self):
        super().__init__()

        self.power_scale = 250.0
        self.fin_height_scale = 0.04
        self.velocity_scale = 3.0

        self.net = nn.Sequential(
            nn.Linear(3, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        x_norm = torch.stack([
            x[:, 0] / self.power_scale,
            x[:, 1] / self.fin_height_scale,
            x[:, 2] / self.velocity_scale
        ], dim=1)

        return self.net(x_norm)
