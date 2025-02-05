import logging
import os
import jinja2
from lib import run_external_applicaton

def before(current_configuration, design_path, output, test_id):
   logging.info(f"before.")

def after(current_configuration, design_path, output, test_id):
   logging.info(f"after.")
