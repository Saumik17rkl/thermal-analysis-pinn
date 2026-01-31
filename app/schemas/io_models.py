"""
Input / Output data models for the thermal analysis API.

These schemas define the expected structure of incoming requests
and outgoing responses. They are intentionally lightweight and
framework-agnostic.
"""

from typing import Dict, Any


class ThermalRequestSchema:
    """
    Schema for thermal analysis request input.
    """

    REQUIRED_FIELDS = [
        "processor",
        "heat_sink",
        "tim",
        "air",
        "ambient",
        "junction_to_case_resistance"
    ]

    @staticmethod
    def validate(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate incoming request payload.

        Raises:
            KeyError: if required fields are missing
            ValueError: if payload is invalid
        """

        if not isinstance(payload, dict):
            raise ValueError("Payload must be a JSON object")

        # -----------------------------
        # Required top-level fields
        # -----------------------------
        for field in ThermalRequestSchema.REQUIRED_FIELDS:
            if field not in payload:
                raise KeyError(field)

        def require_number(value, name, allow_zero=False):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be a number")
            if not allow_zero and value <= 0:
                raise ValueError(f"{name} must be > 0")

        # -----------------------------
        # Processor
        # -----------------------------
        processor = payload["processor"]
        require_number(processor["die_length"], "processor.die_length")
        require_number(processor["die_width"], "processor.die_width")
        require_number(processor["power"], "processor.power", allow_zero=False)

        # -----------------------------
        # Heat sink
        # -----------------------------
        hs = payload["heat_sink"]
        require_number(hs["sink_length"], "heat_sink.sink_length")
        require_number(hs["sink_width"], "heat_sink.sink_width")
        require_number(hs["base_thickness"], "heat_sink.base_thickness")
        require_number(hs["number_of_fins"], "heat_sink.number_of_fins")
        require_number(hs["fin_thickness"], "heat_sink.fin_thickness")
        require_number(hs["fin_height"], "heat_sink.fin_height")

        # -----------------------------
        # TIM
        # -----------------------------
        tim = payload["tim"]
        require_number(tim["thermal_conductivity"], "tim.thermal_conductivity")
        require_number(tim["thickness"], "tim.thickness")

        # -----------------------------
        # Air
        # -----------------------------
        air = payload["air"]
        require_number(air["velocity"], "air.velocity")
        require_number(air["thermal_conductivity"], "air.thermal_conductivity")
        require_number(air["kinematic_viscosity"], "air.kinematic_viscosity")
        require_number(air["prandtl_number"], "air.prandtl_number")

        # -----------------------------
        # Ambient + Rjc
        # -----------------------------
        require_number(payload["ambient"]["temperature"], "ambient.temperature", allow_zero=True)
        require_number(payload["junction_to_case_resistance"], "junction_to_case_resistance")

        return payload

class ThermalValidationError(ValueError):
    pass

class MissingFieldError(KeyError):
    pass

class ThermalResponseSchema:
    """
    Schema for thermal analysis response output.
    """

    @staticmethod
    def build(
        r_tim: float,
        r_conduction: float,
        r_convection: float,
        r_heat_sink: float,
        r_total: float,
        junction_temperature: float
    ) -> Dict[str, Any]:
        """
        Build standardized API response.
        """

        return {
            "resistances": {
                "tim": r_tim,
                "conduction": r_conduction,
                "convection": r_convection,
                "heat_sink": r_heat_sink,
                "total": r_total
            },
            "junction_temperature": junction_temperature
        }
