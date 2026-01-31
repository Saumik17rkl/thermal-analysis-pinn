"""
Configuration constants for the thermal analysis application.

Centralizes all default values, physical constants, and
tunable parameters for easy maintenance and consistency.
"""

# -----------------------------
# Material Properties
# -----------------------------
DEFAULT_THERMAL_CONDUCTIVITY_ALUMINUM = 167.0  # W/m·K (Al 6061-T6)
DEFAULT_THERMAL_CONDUCTIVITY_TIM = 4.0        # W/m·K (typical TIM)

# -----------------------------
# Heat Sink Geometry Defaults
# -----------------------------
DEFAULT_FIN_THICKNESS = 0.0008      # m (0.8 mm)
DEFAULT_BASE_THICKNESS = 0.0025     # m (2.5 mm)
MIN_FIN_SPACING_RATIO = 0.1         # Minimum spacing/fin_thickness ratio

# -----------------------------
# Thermal Analysis Parameters
# -----------------------------
DEFAULT_JUNCTION_TO_CASE_RESISTANCE = 0.1  # °C/W
AMBIENT_TEMPERATURE_DEFAULT = 25.0         # °C

# -----------------------------
# Convection Model Parameters
# -----------------------------
REYNOLDS_LAMINAR_THRESHOLD = 2300    # Flow regime transition
DEFAULT_FIN_EFFICIENCY_THRESHOLD = 0.8  # For validation

# -----------------------------
# API Configuration
# -----------------------------
API_VERSION = "v1"
API_TITLE = "Thermal Analysis API"
API_DESCRIPTION = "Physics-based thermal resistance and junction temperature analysis"

# -----------------------------
# Validation Tolerances
# -----------------------------
RELATIVE_TOLERANCE = 1e-6           # For numerical comparisons
ABSOLUTE_TOLERANCE = 1e-9           # For near-zero values

# -----------------------------
# PINN Training Configuration
# -----------------------------
PINN_CONFIG = {
    "learning_rate": 1e-3,
    "epochs": 10000,
    "batch_size": 1000,
    "loss_weights": {
        "pde": 1.0,
        "base_flux": 10.0,
        "convection": 5.0,
        "lumped": 2.0
    },
    "validation_frequency": 500,
    "checkpoint_frequency": 1000
}

# -----------------------------
# Performance Settings
# -----------------------------
MAX_CACHE_SIZE = 128                # For LRU caching
REQUEST_TIMEOUT = 30                # seconds
MAX_POWER_DISSIPATION = 1000.0      # W (safety limit)

# -----------------------------
# Environment Variables
# -----------------------------
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# -----------------------------
# Logging Configuration
# -----------------------------
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
