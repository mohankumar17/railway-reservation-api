import time
from app.utils.database_connection import database_connect
from app.utils.custom_exception import MIMETYPE_NOT_SUPPORTED

def create_reservations(request):

    if request.is_json:
        request_body = request.json
    else:
        raise MIMETYPE_NOT_SUPPORTED(f"Request Body's Media Type is not supported. Reservation system accepts only application/json MIME Type")

    dbConn = database_connect()
    dbCurr = dbConn.cursor()

    reservation_data = {	
        "reservationDate": time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()),
        "travelDate": request_body.get("travelDate"),
        "sourceStation": request_body.get("sourceStation"),
        "destinationStation": request_body.get("destinationStation"),
        "paymentMethod": request_body.get("paymentMethod"),
        "totalFare": request_body.get("totalFare"),
        "bookingStatus": "NotConfirmed" if request_body.get("status") is None else request_body.get("status"),
        "trainId": request_body.get("trainId")
    }
    
    reservationInsertQuery = f"""
    INSERT INTO RAILWAY_RESERVATIONS(reservation_date,travel_date,source_station,\
    destination_station,payment_method,total_fare,booking_status,train_id)\
    VALUES('{reservation_data.get("reservationDate")}','{reservation_data.get("travelDate")}',\
    '{reservation_data.get("sourceStation")}','{reservation_data.get("destinationStation")}',\
    '{reservation_data.get("paymentMethod")}',{reservation_data.get("totalFare")},\
    '{reservation_data.get("bookingStatus")}','{reservation_data.get("trainId")}')\
    """

    dbCurr.execute(reservationInsertQuery)

    reservationId = dbCurr.lastrowid
    
    columns = ['reservation_id','passenger_id','name','age','gender','coach_no','seat_no','class_type']
    passengers_data = list(map(lambda passenger: [reservationId, passenger.get("passengerId"), passenger.get("name"), passenger.get("age"), passenger.get("gender"), passenger.get("coachNumber"), passenger.get("seatNumber"), passenger.get("classType")], request_body.get("passengers")))
    
    passengersInsertQuery = f"""
    INSERT INTO TICKET_PASSENGER_DETAILS({','.join(columns)})\
    VALUES({('%s,'*len(columns))[:-1]})\
    """

    dbCurr.executemany(passengersInsertQuery, passengers_data)
    dbConn.commit()

    response = {
        "message": "Reservation is successful",
        "reservationId": reservationId,
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }

    dbConn.close()

    return response, 201