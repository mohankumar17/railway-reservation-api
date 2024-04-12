import yaml
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Reading Configuration Properties from YAML File
config = {}
with open("config/dev.yaml") as config_file:
    config = yaml.safe_load(config_file)