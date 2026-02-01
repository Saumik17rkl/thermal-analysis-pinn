"""

Flask application entry point.



- Uses application factory pattern

- Supports environment-based configuration

- Exposes health check endpoint

"""



import os

from flask import Flask, jsonify



from routes import thermal_bp





def create_app() -> Flask:

    """

    Application factory.

    """

    app = Flask(__name__)



    # Basic configuration

    app.config["JSON_SORT_KEYS"] = False



    # Register blueprints

    app.register_blueprint(thermal_bp)



    # Health check (important)

    @app.route("/health", methods=["GET"])

    def health_check():

        return jsonify(

            {

                "status": "ok",

                "service": "thermal-analysis-api"

            }

        ), 200



    return app





if __name__ == "__main__":

    app = create_app()



    host = os.getenv("FLASK_HOST", "0.0.0.0")

    port = int(os.getenv("FLASK_PORT", 5000))

    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"



    app.run(host=host, port=port, debug=debug)

