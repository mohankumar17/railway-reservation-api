import mysql.connector as db
from flask import current_app

def database_connect():

    host = current_app.config.get("DB_HOST")
    port = current_app.config.get("DB_PORT")
    schema = current_app.config.get("DB_SCHEMA")
    username = current_app.config.get("DB_USERNAME")
    password = current_app.config.get("DB_PASSWORD")

    dbConn = db.connect(host = host, port = port, user = username, passwd = password, database = schema)

    return dbConn