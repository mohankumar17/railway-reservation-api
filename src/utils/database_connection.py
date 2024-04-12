import mysql.connector as db
from utils.global_config import config

def database_connect():
        
    host = config["db"]["host"]
    port = config["db"]["port"]
    schema = config["db"]["schema"]
    username = config["db"]["username"]
    password = config["db"]["password"]

    dbConn = db.connect(host = host, port = port, user = username, passwd = password, database = schema)

    return dbConn