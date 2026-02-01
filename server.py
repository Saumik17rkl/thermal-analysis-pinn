"""
Production server runner for Windows compatibility.
"""

from waitress import serve
from app.main import create_app

if __name__ == "__main__":
    app = create_app()
    print("🚀 Starting Thermal Analysis API on http://localhost:5000")
    print("📊 Health check: http://localhost:5000/health")
    print("🔥 Thermal analysis: http://localhost:5000/thermal/solve")
    serve(app, host="0.0.0.0", port=5000)
