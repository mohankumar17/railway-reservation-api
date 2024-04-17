from flask import Blueprint, request
import time
import uuid
from app.config import Config

from app.services.create_reservation import create_reservations
from app.services.get_reservation import get_reservations_by_id, get_reservations_by_status
from app.services.update_reservation import update_reservations
from app.services.delete_reservation import delete_reservations
from app.utils.custom_exception import RESERVATION_NOT_FOUND, MIMETYPE_NOT_SUPPORTED
from pydantic import ValidationError

reservations_bp = Blueprint('reservations', __name__)
logger = Config.logger

# Routers
@reservations_bp.get("/api/reservations/<reservationId>")
def get_reservations_id_route(reservationId):
    return get_reservations_by_id(reservationId)

@reservations_bp.get("/api/reservations")
def get_reservations_status_route():
    return get_reservations_by_status(request)

@reservations_bp.post("/api/reservations")
def create_reservations_route():
    return create_reservations(request)

@reservations_bp.put("/api/reservations/<reservationId>")
def update_reservations_route(reservationId):
    return update_reservations(request, reservationId)

@reservations_bp.delete("/api/reservations/<reservationId>")
def delete_reservations_route(reservationId):
    return delete_reservations(reservationId)

############################################################################
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
        "message": errorDetails.get("message"),
        "description": errorDetails.get("description"),
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
        "transactionId": str(uuid.uuid4())
    }
    logger.error(error_response)
    return error_response

@reservations_bp.errorhandler(Exception)
def global_error_handler(error):
    errorDetails = {
        "message": "Reservation server error",
        "description": str(error)
    }
    status_code = 500
    response = error_response(errorDetails)
    return response, status_code

@reservations_bp.errorhandler(RESERVATION_NOT_FOUND)
def not_found_error_handler(error):
    errorDetails = {
        "message": "Reservation entry not found",
        "description": str(error)
    }
    status_code = 404
    response = error_response(errorDetails)
    return response, status_code

@reservations_bp.errorhandler(MIMETYPE_NOT_SUPPORTED)
def mediatype_error_handler(error):
    errorDetails = {
        "message": "Unsupported Media Type",
        "description": str(error)
    }
    status_code = 415
    response = error_response(errorDetails)
    return response, status_code

@reservations_bp.errorhandler(ValidationError)
def validation_error_handler(error):
    errorDetails = {
        "message": "Input data validation failed",
        "description": str(error)
    }
    status_code = 400
    response = error_response(errorDetails)
    return response, status_code
