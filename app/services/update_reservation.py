import time
from app.utils.database_connection import database_connect
from app.utils.custom_exception import RESERVATION_NOT_FOUND, MIMETYPE_NOT_SUPPORTED
from app.utils.validation_models import Reservation, Passenger

def update_reservations(request, reservationId):

    if request.is_json:
        request_body = request.json
    else:
        raise MIMETYPE_NOT_SUPPORTED(f"Request Body's Media Type is not supported. Reservation system accepts only application/json MIME Type")
    
    updatedOn = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())

    passengersList = list(map(lambda passenger: Passenger(passengerId=passenger.get("passengerId"),
                                                          name=passenger.get("name"),
                                                          age=passenger.get("age"),
                                                          gender=passenger.get("gender"),
                                                          classType=passenger.get("classType"),
                                                          coachNumber=passenger.get("coachNumber"), 
                                                          seatNumber=passenger.get("seatNumber")),
                                                        request_body.get("passengers")))
    
    reservation = Reservation(travelDate=request_body.get("travelDate"),
                              sourceStation=request_body.get("sourceStation"),
                              destinationStation=request_body.get("destinationStation"),
                              paymentMethod=request_body.get("paymentMethod"),
                              totalFare=request_body.get("totalFare"),
                              status="NotConfirmed" if request_body.get("status") is None else request_body.get("status"),
                              trainId=request_body.get("trainId"),
                              passengers=passengersList)
    
    dbConn = database_connect()
    dbCurr = dbConn.cursor()

    reservationUpdateQuery = f"""
    UPDATE RAILWAY_RESERVATIONS\
    SET payment_method='{reservation.paymentMethod}',\
	total_fare={reservation.totalFare},\
	booking_status='{reservation.status}',\
	train_id='{reservation.trainId}',\
	travel_date='{reservation.travelDate}',\
	source_station='{reservation.sourceStation}',\
	destination_station='{reservation.destinationStation}',\
	updated_on='{updatedOn}'\
    WHERE reservation_id={reservationId}\
    """

    dbCurr.execute(reservationUpdateQuery)

    rowsUpdated = dbCurr.rowcount

    if rowsUpdated == 0:
        dbConn.close()
        raise RESERVATION_NOT_FOUND(f"Reservation with ID: {reservationId} is not found in the system")
    
    passenger_columns = ['name','age','gender','class_type','coach_no','seat_no','updated_on']
    passengers = list(map(lambda passenger: [passenger.name, passenger.age, passenger.gender,
                                             passenger.classType, passenger.coachNumber, passenger.seatNumber,
                                             updatedOn, passenger.passengerId],
                                        reservation.passengers))

    passengersUpdateQuery = f"""
    UPDATE TICKET_PASSENGER_DETAILS\
    SET {','.join((col + '=%s') for col in passenger_columns)}\
    WHERE reservation_id={reservationId} AND passenger_id=%s\
    """

    dbCurr.executemany(passengersUpdateQuery, passengers)
    dbConn.commit()

    response = {
        "message": "Reservation details updated successfully",
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }

    dbConn.close()

    return response, 200