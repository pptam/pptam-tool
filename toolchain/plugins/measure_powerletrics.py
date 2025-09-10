import logging
import os
import jinja2
from lib import run_external_applicaton
import requests
import shutil
import json
import zipfile

# Refrernece for tool
# https://github.com/green-kernel/powerletrics
# Need to install all before

#def before(current_configuration, design_path, output, test_id):
def run(current_configuration, design_path, output, test_id):
    logging.info(f"Starting background PPTAM-Client")

    command_start_pptam_client = f"python3 ./pptam-client/pptam-client.py &" 
    run_external_applicaton(command_start_pptam_client)

    logging.info(f"Starting collecting data for PPTAM-CLIENT")
    last_folder = os.path.basename(output)
    url = "http://" + current_configuration["docker_stats_hostname"] + ":5888/start/" + last_folder
    try:
        response = requests.get(url)
        if response.status_code not in [200, 201]:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
        logging.info(f"--> Started")
    except requests.RequestException as e:
        raise Exception(f"Error while making request: {repr(e)}")

def after(current_configuration, design_path, output, test_id):
    logging.info(f"Killing powerletrics process")
    url = "http://" +current_configuration["docker_stats_hostname"] + ":5888/stop"
    try:
        response = requests.get(url)
        if response.status_code not in [200, 201]:
            raise Exception(f"Request failed with status code")
        logging.info(f"--> Stopped ")
    except requests.RequestException as e:
        raise Exception(f"Error while making request: {repr(e)}")


def teardown(current_configuration, design_path, output, test_id):
    logging.info(f"Downloading data from the client of {test_id}")
    last_folder = os.path.basename(output)
    url = "http://" + current_configuration["docker_stats_hostname"] + ":5888/download/" + last_folder
    output_file = "client-data.zip"
    try:
        response = requests.get(url, stream=True)
        if response.status_code not in [200, 201]:
            raise Exception(f"Request of download failed with status code {response.status_code}: {response.text}")
        logging.info(f"--> Extraction of download file")
        with open(os.path.join(output, output_file), "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Downloaded ZIP file: {output_file}")
        extract_and_copy(output,output_file)
        logging.info(f"Kill PPTAM-CLIENT")
        run_external_applicaton(f'kill $(pgrep -f pptam-client)', False)

    except requests.RequestException as e:
        raise Exception(f"Error while making request: {repr(e)}")


# DEFINE MOMENT TO DOWNLOAD THE DATA


#def download_zip(url, output_file):
#    """Download ZIP file from a URL."""
#    response = requests.get(url, stream=True)
#    if response.status_code == 200:
#        with open(output_file, "wb") as f:
#            for chunk in response.iter_content(chunk_size=8192):
#                f.write(chunk)
#        logging.info(f"Downloaded ZIP file: {output_file}")
#    else:
#        raise Exception(f"Failed to download ZIP. Status code: {response.status_code}")

def extract_and_copy(folder_path: str, file_name: str):
    
    logging.info(f"Extract to {folder_path}  the zip: {file_name}")
    #folder_path = os.path.basename(folder_path)
    file_path = os.path.join(folder_path, file_name)
    logging.info(f"File path: {file_path} does not exist.")
    logging.info(f"Error: {file_path} does not exist.")
    
    if not os.path.exists(folder_path):
        logging.info(f"Error: {folder_path} does not exist.")
        return
    
    if not zipfile.is_zipfile(file_path):
        logging.info(f"Error: {file_path} is not a valid ZIP file.")
        return
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_path)
        logging.info(f"Successfully extracted {file_path} in {folder_path}")
    except Exception as e:
        logging.info(f"Error extracting file: {e}")
