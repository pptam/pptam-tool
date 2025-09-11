import logging
import os
import jinja2
from lib import run_external_application
import requests
import json

# Refrernece for tool
# https://github.com/green-kernel/powerletrics
# Need to install all before

def before(current_configuration, design_path, output, test_id):
   logging.info(f"Starting background process of powerletrics")
   #output_file = f"{output}/powerletrics.xml"
   #sample_time = 500 # in milliseconds
   #run_external_application(
    #    f'powerletrics --format plist --output-file {output_file} --sample-rate {sample_time} &', False)
   # how to get the pid and use to stop in the end?
   url = current_configuration["docker_stats_hostname"] + ":5888/start/" + output
   response = requests.get(url)

def after(current_configuration, design_path, output, test_id):
   logging.info(f"Killing powerletrics process")
   # close the process in background and process data, remove other process data and let only containers data
   # kill $(pgrep -f powerletrics)
   #run_external_application(
   #     f'kill $(pgrep -f powerletrics)', False)
   url = current_configuration["docker_stats_hostname"] + ":5888/stop"
   response = requests.get(url)
   #Download file?

