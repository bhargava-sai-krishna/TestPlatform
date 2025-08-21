from flask import Flask
from flask_migrate import Migrate
from app.config import Config
from app.extensions import db, jwt, init_cors
from app.routes.auth import bp as auth_bp
from flasgger import Swagger
from flask.cli import FlaskGroup

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Swagger(app)

    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)
    init_cors(app, [o.strip() for o in app.config.get("CORS_ORIGINS","").split(",") if o.strip()])

    with app.app_context():
        from app import models  # noqa
        db.create_all()

    app.register_blueprint(auth_bp)

    @app.get("/health")
    def health():
        """
        Health check endpoint
        ---
        tags:
          - System
        responses:
          200:
            description: Returns the status of the service
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    status:
                      type: string
                      example: ok
                    service:
                      type: string
                      example: flask_auth
        """
        return {"status": "ok", "service": "flask_auth"}
    
    @app.route("/test")
    def serve_test():
        """
        Serve test HTML page
        ---
        tags:
          - System
        responses:
          200:
            description: Returns a static HTML test page
            content:
              text/html:
                schema:
                  type: string
                  example: "<!DOCTYPE html><html><body><h3>Test page</h3></body></html>"
        """
        return app.send_static_file("test.html")

    return app


app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=True)
