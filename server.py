"""
Production server runner for Windows and cloud platforms.
"""

import os
from waitress import serve
from app.main import create_app

if __name__ == "__main__":
    app = create_app()
    
    # Use PORT from environment (Render, Heroku) or default to 5000
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Thermal Analysis API on http://{host}:{port}")
    print(f"📊 Health check: http://{host}:{port}/health")
    print(f"🔥 Thermal analysis: http://{host}:{port}/thermal/solve")
    
    serve(app, host=host, port=port)
