import mysql.connector as db
from app.config import Config

def database_connect():

    host = Config.DB_HOST
    port = Config.DB_PORT
    schema = Config.DB_SCHEMA
    username = Config.DB_USERNAME
    password = Config.DB_PASSWORD

    dbConn = db.connect(host = host, port = port, user = username, passwd = password, database = schema)

    return dbConn