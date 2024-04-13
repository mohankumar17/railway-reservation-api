import pandas as pd
from time import strftime
from app.utils.database_connection import database_connect
from app.utils.custom_exception import RESERVATION_NOT_FOUND

def get_reservations_db(selectQuery):

    dbConn = database_connect()
    df = pd.read_sql(sql=selectQuery, con=dbConn)
    response = []

    if df.shape[0] == 0:
        dbConn.close()
        raise RESERVATION_NOT_FOUND(f"No reservation details found")
    else:
        result_df = df.groupby(by='reservation_id').agg(lambda x: list(x))

        response = list(map(lambda reservationId: {
            "reservationId": int(reservationId),
            "reservationDate": result_df.at[reservationId,"reservation_date"][0],
            "travelDate": None if result_df.at[reservationId, 'travel_date'][0] is None else result_df.at[reservationId, 'travel_date'][0].strftime("%Y-%m-%d"),
            "sourceStation": result_df.at[reservationId, 'source_station'][0],
            "destinationStation": result_df.at[reservationId, 'destination_station'][0],
            "paymentMethod": result_df.at[reservationId, 'payment_method'][0],
            "totalFare": float(result_df.at[reservationId, 'total_fare'][0]),
            "status": result_df.at[reservationId, 'booking_status'][0],
            "trainId": result_df.at[reservationId, 'train_id'][0],
            "passengers": list(map(lambda passenger: {
                "passengerId": result_df.at[reservationId, 'passenger_id'][passenger],
                "name": result_df.at[reservationId, 'name'][passenger],
                "age": result_df.at[reservationId,"age"][passenger],
                "gender": result_df.at[reservationId,"gender"][passenger],
                "coachNumber": result_df.at[reservationId,"coach_no"][passenger],
                "seatNumber": result_df.at[reservationId,"seat_no"][passenger],
                "classType": result_df.at[reservationId,"class_type"][passenger]
            }, range(len(result_df.at[reservationId, 'passenger_id']))))
        },result_df.index))
    
    dbConn.close()
    return response

def get_reservations_by_status(request):

    bookingStatus = request.args["status"]
    
    selectQuery = f"""
    SELECT rr.reservation_id, rr.reservation_date, rr.travel_date, rr.source_station, rr.destination_station,\
    rr.payment_method, rr.total_fare, rr.booking_status, rr.train_id, tpd.passenger_id, tpd.name, tpd.age,\
    tpd.gender, tpd.coach_no, tpd.seat_no, tpd.class_type\
    FROM RAILWAY_RESERVATIONS rr\
    INNER JOIN TICKET_PASSENGER_DETAILS tpd\
    ON rr.reservation_id=tpd.reservation_id\
    WHERE rr.booking_status='{bookingStatus}'\
    """

    return get_reservations_db(selectQuery), 200

def get_reservations_by_id(reservationId):

    selectQuery = f"""
    SELECT rr.reservation_id, rr.reservation_date, rr.travel_date, rr.source_station, rr.destination_station,\
    rr.payment_method, rr.total_fare, rr.booking_status, rr.train_id, tpd.passenger_id, tpd.name, tpd.age,\
    tpd.gender, tpd.coach_no, tpd.seat_no, tpd.class_type\
    FROM RAILWAY_RESERVATIONS rr\
    INNER JOIN TICKET_PASSENGER_DETAILS tpd\
    ON rr.reservation_id=tpd.reservation_id\
    WHERE rr.reservation_id={reservationId}\
    """

    return get_reservations_db(selectQuery)[0], 200