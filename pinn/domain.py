"""
Spatial domain definition for PINN training.

Defines the heat sink geometry and provides utilities
to sample interior and boundary points for physics-based learning.
"""

import numpy as np


class HeatSinkDomain:
    """
    Heat sink spatial domain for PINN.

    Coordinate system:
    - x: sink length direction
    - y: sink width direction
    - z: vertical direction (base -> fin tip)
    """

    def __init__(
        self,
        sink_length: float,
        sink_width: float,
        fin_height: float,
        base_thickness: float
    ):
        if sink_length <= 0:
            raise ValueError("Sink length must be positive")
        if sink_width <= 0:
            raise ValueError("Sink width must be positive")
        if fin_height <= 0:
            raise ValueError("Fin height must be positive")
        if base_thickness <= 0:
            raise ValueError("Base thickness must be positive")

        self.x_min = 0.0
        self.x_max = sink_length

        self.y_min = 0.0
        self.y_max = sink_width

        self.z_min = 0.0
        self.z_max = base_thickness + fin_height

        self.base_z = base_thickness

    def sample_interior(self, n_points: int) -> np.ndarray:
        """
        Sample interior points inside the heat sink volume.

        Returns:
            Array of shape (n_points, 3) → (x, y, z)
        """

        if n_points <= 0:
            raise ValueError("Number of points must be positive")

        x = np.random.uniform(self.x_min, self.x_max, n_points)
        y = np.random.uniform(self.y_min, self.y_max, n_points)
        z = np.random.uniform(self.z_min, self.z_max, n_points)

        return np.column_stack((x, y, z))

    # Boundary sampling

    def sample_base(self, n_points: int) -> np.ndarray:
        """
        Sample points on the die–base interface (heat flux boundary).
        """

        if n_points <= 0:
            raise ValueError("Number of points must be positive")

        x = np.random.uniform(self.x_min, self.x_max, n_points)
        y = np.random.uniform(self.y_min, self.y_max, n_points)
        z = np.full(n_points, self.base_z)

        return np.column_stack((x, y, z))

    def sample_top(self, n_points: int) -> np.ndarray:
        """
        Sample points on the top fin surface (convective boundary).
        """

        if n_points <= 0:
            raise ValueError("Number of points must be positive")

        x = np.random.uniform(self.x_min, self.x_max, n_points)
        y = np.random.uniform(self.y_min, self.y_max, n_points)
        z = np.full(n_points, self.z_max)

        return np.column_stack((x, y, z))

    def sample_side_walls(self, n_points: int) -> np.ndarray:
        """
        Sample points on the side walls (assumed convective or symmetry BC).
        """

        if n_points <= 0:
            raise ValueError("Number of points must be positive")

        points = []

        for _ in range(n_points):
            face = np.random.choice(["x0", "x1", "y0", "y1"])
            z = np.random.uniform(self.z_min, self.z_max)

            if face == "x0":
                points.append([self.x_min, np.random.uniform(self.y_min, self.y_max), z])
            elif face == "x1":
                points.append([self.x_max, np.random.uniform(self.y_min, self.y_max), z])
            elif face == "y0":
                points.append([np.random.uniform(self.x_min, self.x_max), self.y_min, z])
            else:
                points.append([np.random.uniform(self.x_min, self.x_max), self.y_max, z])

        return np.array(points)
