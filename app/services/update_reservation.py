import time
from app.utils.database_connection import database_connect
from app.utils.custom_exception import RESERVATION_NOT_FOUND, MIMETYPE_NOT_SUPPORTED

def update_reservations(request, reservationId):

    if request.is_json:
        request_body = request.json
    else:
        raise MIMETYPE_NOT_SUPPORTED(f"Request Body's Media Type is not supported. Reservation system accepts only application/json MIME Type")

    dbConn = database_connect()
    dbCurr = dbConn.cursor()

    reservation_data = {
        "updatedOn": time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()),
        "travelDate": request_body.get("travelDate"),
        "sourceStation": request_body.get("sourceStation"),
        "destinationStation": request_body.get("destinationStation"),
        "paymentMethod": request_body.get("paymentMethod"),
        "totalFare": request_body.get("totalFare"),
        "bookingStatus": "NotConfirmed" if request_body.get("status") is None else request_body.get("status"),
        "trainId": request_body.get("trainId")
    }
    
    reservationUpdateQuery = f"""
    UPDATE RAILWAY_RESERVATIONS\
    SET payment_method='{reservation_data.get("paymentMethod")}',\
	total_fare={reservation_data.get("totalFare")},\
	booking_status='{reservation_data.get("bookingStatus")}',\
	train_id='{reservation_data.get("trainId")}',\
	travel_date='{reservation_data.get("travelDate")}',\
	source_station='{reservation_data.get("sourceStation")}',\
	destination_station='{reservation_data.get("destinationStation")}',\
	updated_on='{reservation_data.get("updatedOn")}'\
    WHERE reservation_id={reservationId}\
    """

    dbCurr.execute(reservationUpdateQuery)

    rowsUpdated = dbCurr.rowcount

    if rowsUpdated == 0:
        dbConn.close()
        raise RESERVATION_NOT_FOUND(f"Reservation with ID: {reservationId} is not found in the system")
    
    columns = ['name','age','gender','coach_no','seat_no','class_type','updated_on']
    passengers_data = list(map(lambda passenger: [passenger.get("name"), passenger.get("age"), passenger.get("gender"), passenger.get("coachNumber"), passenger.get("seatNumber"), passenger.get("classType"), reservation_data.get("updatedOn"), passenger.get("passengerId")], request_body.get("passengers")))

    passengersUpdateQuery = f"""
    UPDATE TICKET_PASSENGER_DETAILS\
    SET {','.join((col + '=%s') for col in columns)}\
    WHERE reservation_id={reservationId} AND passenger_id=%s\
    """

    dbCurr.executemany(passengersUpdateQuery, passengers_data)
    dbConn.commit()

    response = {
        "message": "Reservation details updated successfully",
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }

    dbConn.close()

    return response, 200