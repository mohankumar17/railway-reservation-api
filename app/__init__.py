from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.reservations import reservations_bp
    app.register_blueprint(reservations_bp)

    return app