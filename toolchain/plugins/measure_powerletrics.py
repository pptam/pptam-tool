import logging
import os
import jinja2
from lib import run_external_applicaton

# Refrernece for tool
# https://github.com/green-kernel/powerletrics
# Need to install all before

def before(current_configuration, design_path, output, test_id):
   logging.info(f"Starting background process of powerletrics")
   output_file = f"{output}/powerletrics.xml"
   sample_time = 500 # in milliseconds
   run_external_applicaton(
        f'powerletrics --format plist --output-file {output_file} --sample-rate {sample_time} &', False)
   # how to get the pid and use to stop in the end?

def after(current_configuration, design_path, output, test_id):
   logging.info(f"Killing powerletrics process")
   # close the process in background and process data, remove other process data and let only containers data
   # kill $(pgrep -f powerletrics)
   run_external_applicaton(
        f'kill $(pgrep -f powerletrics)', False)

