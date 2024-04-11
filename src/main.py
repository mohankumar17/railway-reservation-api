from flask import Flask, request
import yaml
from implementations.get_reservation import get_reservations_by_id
from utils.custom_exception import RESERVATION_NOT_FOUND

# Reading Configuration Properties from YAML File
with open("config/dev.yaml") as config_file:
    config = yaml.safe_load(config_file)

app = Flask(__name__)

@app.errorhandler(Exception)
def global_error_handler(error):
    response = {
        "message": "Reservation server error",
        "description": str(error)
    }
    status_code = 500
    return response, status_code

@app.errorhandler(RESERVATION_NOT_FOUND)
def not_found_error_handler(error):
    response = {
        "message": "Reservation entry not found",
        "description": str(error)
    }
    status_code = 404
    return response, status_code

@app.get("/api/reservations/<reservationId>")
def get_reservations(reservationId):
    return get_reservations_by_id(reservationId, config)

if __name__ == '__main__':
   app.run(host=config["http"]["host"], port=config["http"]["port"], debug=True)