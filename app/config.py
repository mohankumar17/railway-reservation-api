import yaml
import logging

class Config:
    with open("config/dev.yaml") as config_file:
        properties = yaml.safe_load(config_file)
    
    HTTP_HOST = properties["http"]["host"]
    HTTP_PORT = properties["http"]["port"]

    DB_HOST = properties["db"]["host"]
    DB_PORT = properties["db"]["port"]
    DB_SCHEMA = properties["db"]["schema"]
    DB_USERNAME = properties["db"]["username"]
    DB_PASSWORD = properties["db"]["password"]

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)