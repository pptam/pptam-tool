import logging
import os
import subprocess

def run_external_application(command, fail_if_result_not_zero=True):
    current_folder = os.getcwd()
    logging.debug(f"Executing {command} in {current_folder}.")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        logging.debug(f"stdout: {result.stdout}")
    if result.stderr:
        logging.debug(f"stderr: {result.stderr}")
    if fail_if_result_not_zero and result.returncode != 0:
        logging.fatal(f"Could not execute {command}: {result.returncode}.")
        raise RuntimeError
    else:
        return result.returncode

def replace_values_in_file(file, replacements):
    for replacement in replacements:
        replace_value_in_file(file, replacement["search_for"], replacement["replace_with"])

def replace_value_in_file(file, search_for, replace_with):
    with open(file, "r") as f:
        content = f.read()
        content = content.replace(search_for, replace_with)
    with open(file, "w") as f:
        f.write(content)
