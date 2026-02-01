"""

Service layer for the thermal analysis application.



This package contains orchestration logic that connects

API routes with the core thermal physics model.

"""



from .thermal_service import run_thermal_analysis



__all__ = ["run_thermal_analysis"]

