"""
Core thermal physics package.

This package contains the validated, deterministic thermal model:
- Geometry calculations
- Thermal resistances (TIM, conduction, convection)
- Thermal resistance network
- Final junction temperature solver

No Flask, no ML, no I/O should appear here.
"""

from .constants import *
from .geometry import *
from .tim import compute_tim_resistance
from .conduction import compute_conduction_resistance
from .convection import compute_convection_resistance
from .resistance_network import compute_total_resistance
from .solver import compute_junction_temperature
