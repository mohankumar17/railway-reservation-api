import pandas as pd
from time import strftime
from utils.database_connection import database_connect
from utils.custom_exception import RESERVATION_NOT_FOUND

def get_reservations_by_id(reservationId, config):

    dbConn = database_connect(config)

    selectQuery = f"SELECT * FROM RAILWAY_RESERVATIONS where reservation_id = {reservationId};"
    result_df = pd.read_sql(sql=selectQuery, con=dbConn)

    if result_df.shape[0] == 0:
        raise RESERVATION_NOT_FOUND(f"No reservation details found for ID: {reservationId}")
    else:
        response = {
            "reservationId": int(result_df.at[0, 'reservation_id']),
            "reservationDate": result_df.at[0, 'reservation_date'].strftime("%Y-%m-%d"),
            "travelDate": None if result_df.at[0, 'travel_date'] is None else result_df.at[0, 'travel_date'].strftime("%Y-%m-%d"),
            "sourceStation": result_df.at[0, 'source_station'],
            "destinationStation": result_df.at[0, 'destination_station'],
            "paymentMethod": result_df.at[0, 'payment_method'],
            "totalFare": float(result_df.at[0, 'total_fare']),
            "status": result_df.at[0, 'booking_status'],
            "trainId": result_df.at[0, 'train_id']
        }
        status_code = 200

    return response, status_code