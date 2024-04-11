import mysql.connector as db

def database_connect(config):
        
    host = config["db"]["host"]
    port = config["db"]["port"]
    schema = config["db"]["schema"]
    username = config["db"]["username"]
    password = config["db"]["password"]

    dbConn = db.connect(host = host, port = port, user = username, passwd = password, database = schema)

    return dbConn