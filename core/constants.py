"""
Physical and material constants for the thermal model.

This module contains only fixed parameters and default reference values.
No computations should be performed here.
"""

# Processor / Package


# Junction-to-case thermal resistance (from datasheet / reference)
R_JC = 0.1  # °C/W



# Thermal Interface Material (TIM)


TIM_THERMAL_CONDUCTIVITY = 4.0      # W/m·K
TIM_THICKNESS = 0.0001              # m (0.1 mm)



# Heat Sink Material (Al 6061-T6)

ALUMINUM_THERMAL_CONDUCTIVITY = 167.0  # W/m·K



# Air Properties at 25°C

AIR_THERMAL_CONDUCTIVITY = 0.0262   # W/m·K
AIR_KINEMATIC_VISCOSITY = 1.57e-5   # m²/s
AIR_PRANDTL_NUMBER = 0.71


# Ambient Conditions

AMBIENT_TEMPERATURE = 25.0  # °C
