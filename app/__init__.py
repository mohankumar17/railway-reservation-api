from flask import Flask
import logging
from app.configuration import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.setLevel(logging.DEBUG)

    from app.routes.reservations import reservations_bp
    app.register_blueprint(reservations_bp)

    return app