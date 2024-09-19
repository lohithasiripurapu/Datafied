from flask import Flask
from app.routes import init_routes

def create_app(config_object='config.Config'):
    """Application Factory to create a Flask app instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions, if any (e.g., database, authentication)
    # Initialize routes
    init_routes(app)
    
    return app
