import logging
import os

def setup_all():
    logging.debug(f"Plugin #{os.path.basename(__file__)}: setup")

def setup():
    logging.debug(f"Plugin #{os.path.basename(__file__)}: setup")
    
def before(current_configuration, output):
    logging.debug(f"Plugin #{os.path.basename(__file__)}: prepare")

def after(current_configuration, output):
    logging.debug(f"Plugin #{os.path.basename(__file__)}: after")

def teardown(current_configuration, output):
    logging.debug(f"Plugin #{os.path.basename(__file__)}: teardown")

def teardown_all():
    logging.debug(f"Plugin #{os.path.basename(__file__)}: setup")