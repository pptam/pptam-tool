import logging
import os

def setup():
    logging.debug(f"Plugin #{os.path.basename(__file__)}: setup")
    
def declare_configuration_files():
    return ["docker-compose.yml"]

