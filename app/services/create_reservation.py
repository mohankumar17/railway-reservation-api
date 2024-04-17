import time
from app.utils.database_connection import database_connect
from app.utils.custom_exception import MIMETYPE_NOT_SUPPORTED
from app.utils.validation_models import Reservation, Passenger

def create_reservations(request):

    if request.is_json:
        request_body = request.json
    else:
        raise MIMETYPE_NOT_SUPPORTED(f"Request Body's Media Type is not supported. Reservation system accepts only application/json MIME Type")

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
    
    reservationInsertQuery = f"""
    INSERT INTO RAILWAY_RESERVATIONS(reservation_date,travel_date,source_station,\
    destination_station,payment_method,total_fare,booking_status,train_id)\
    VALUES('{reservation.reservationDate}','{reservation.travelDate}',\
    '{reservation.sourceStation}','{reservation.destinationStation}',\
    '{reservation.paymentMethod}',{reservation.totalFare},\
    '{reservation.status}','{reservation.trainId}')\
    """

    dbCurr.execute(reservationInsertQuery)

    reservationId = dbCurr.lastrowid
    
    passengers_columns = ['reservation_id','passenger_id','name','age','gender','class_type','coach_no','seat_no']
    passengers = list(map(lambda passenger: [reservationId, passenger.passengerId, passenger.name, passenger.age, passenger.gender,
                                             passenger.classType, passenger.coachNumber, passenger.seatNumber],
                                        reservation.passengers))
    
    passengersInsertQuery = f"""
    INSERT INTO TICKET_PASSENGER_DETAILS({','.join(passengers_columns)})\
    VALUES({('%s,'*len(passengers_columns))[:-1]})\
    """

    dbCurr.executemany(passengersInsertQuery, passengers)
    dbConn.commit()

    response = {
        "message": "Reservation is successful",
        "reservationId": reservationId,
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }

    dbConn.close()

    return response, 201