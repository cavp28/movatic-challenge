from flask import Flask
from app.config import Config
from app.extensions import db
from app.api import bp as api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register API blueprint
    app.register_blueprint(api_bp)

    return app
