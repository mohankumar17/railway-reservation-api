import time
from app.utils.database_connection import database_connect
from app.utils.custom_exception import RESERVATION_NOT_FOUND

def delete_reservations(reservationId):

    dbConn = database_connect()
    dbCurr = dbConn.cursor()
    
    reservationDeleteQuery = f"""
    DELETE FROM RAILWAY_RESERVATIONS WHERE reservation_id={reservationId}\
    """

    dbCurr.execute(reservationDeleteQuery)

    rowsUpdated = dbCurr.rowcount

    if rowsUpdated == 0:
        dbConn.close()
        raise RESERVATION_NOT_FOUND(f"Reservation with ID: {reservationId} is not found in the system")
    
    dbConn.commit()

    response = {
        "message": "Reservation details deleted successfully",
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }

    dbConn.close()

    return response, 200