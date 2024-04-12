from flask import Flask, request
import time
import uuid
from utils.global_config import logger,config
from implementations.get_reservation import get_reservations_by_id
from implementations.create_reservation import create_reservations
from utils.custom_exception import RESERVATION_NOT_FOUND

app = Flask(__name__)

# Routers
@app.get("/api/reservations/<reservationId>")
def get_reservations_route(reservationId):
    return get_reservations_by_id(reservationId)

@app.post("/api/reservations")
def create_reservations_route():
    return create_reservations(request)

'''
Error Handling
    - Global Error Handler: 500
    - Services Unavailable: 503
    - Bad Request: 400
    - Not Found: 404
'''
# Error Handling 
def error_response(errorDetails):
    error_response =  {
        "message": errorDetails["message"],
        "description": errorDetails["description"],
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
        "transactionId": str(uuid.uuid4())
    }
    logger.error(error_response)
    return error_response

@app.errorhandler(Exception)
def global_error_handler(error):
    errorDetails = {
        "message": "Reservation server error",
        "description": str(error)
    }
    status_code = 500
    response = error_response(errorDetails)
    return response, status_code

@app.errorhandler(RESERVATION_NOT_FOUND)
def not_found_error_handler(error):
    errorDetails = {
        "message": "Reservation entry not found",
        "description": str(error)
    }
    status_code = 404
    response = error_response(errorDetails)
    return response, status_code

if __name__ == '__main__':
   app.run(host=config["http"]["host"], port=config["http"]["port"], debug=True)