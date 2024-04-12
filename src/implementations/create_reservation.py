import pandas as pd
import time
from utils.global_config import logger
from utils.database_connection import database_connect

def create_reservations(request):

    if request.is_json:
        request_body = request.json

    dbConn = database_connect()
    dbCurr = dbConn.cursor()

    reservation_data = {	
        "reservationDate": time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()),
        "travelDate": request_body["travelDate"],
        "sourceStation": request_body["sourceStation"],
        "destinationStation": request_body["destinationStation"],
        "paymentMethod": request_body["paymentMethod"],
        "totalFare": request_body["totalFare"],
        "bookingStatus": "NotConfirmed" if request_body["status"] is None else request_body["status"],
        "trainId": request_body["trainId"]
    }
    
    reservationInsertQuery = f'INSERT INTO RAILWAY_RESERVATIONS(reservation_date,travel_date,source_station,'\
                            f'destination_station,payment_method,total_fare,booking_status,train_id)'\
                            f'VALUES("{reservation_data["reservationDate"]}","{reservation_data["travelDate"]}",'\
                            f'"{reservation_data["sourceStation"]}","{reservation_data["destinationStation"]}",'\
                            f'"{reservation_data["paymentMethod"]}",{reservation_data["totalFare"]},'\
                            f'"{reservation_data["bookingStatus"]}","{reservation_data["trainId"]}");'

    dbCurr.execute(reservationInsertQuery)

    reservationId = dbCurr.lastrowid

    '''passengers_data = list(map(lambda passenger: {
        "reservation_id": reservationId,
        "passenger_id": passenger["passengerId"],
        "name": passenger["name"],
        "age": passenger["age"],
        "gender": passenger["gender"],
        "coach_no": passenger["coachNumber"],
        "seat_no": passenger["seatNumber"],
        "class_type": passenger["classType"]
    }, request_body["passengers"]))'''
    
    columns = ['reservation_id','passenger_id','name','age','gender','coach_no','seat_no','class_type']
    passengers_data = list(map(lambda passenger: [reservationId, passenger["passengerId"], passenger["name"], passenger["age"], passenger["gender"], passenger["coachNumber"], passenger["seatNumber"], passenger["classType"]], request_body["passengers"]))
    
    passengersInsertQuery = f"INSERT INTO TICKET_PASSENGER_DETAILS({','.join(columns)})"\
                            f"VALUES({','.join(['%s']*len(columns))});"

    dbCurr.executemany(passengersInsertQuery, passengers_data)
    dbConn.commit()

    response = {
        "message": "Reservation is successful",
        "reservationId": reservationId,
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }

    dbConn.close()

    return response, 201