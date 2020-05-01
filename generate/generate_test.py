#!/usr/bin/env python
 
import os
import shutil
import json
import sys
import shutil
import argparse
import logging
import uuid 
from os import path

def replace_values_in_file(file, replacements):
    for replacement in replacements:       
        replace_value_in_file(file, replacement["search_for"], replacement["replace_with"])

def replace_value_in_file(file, search_for, replace_with):
    with open(file, "r") as f:
        content = f.read()
        content = content.replace(search_for, replace_with)
    with open(file, "w") as f:
        f.write(content)

def generate_test():
    parser = argparse.ArgumentParser(description="Generates test cases.")
    parser.add_argument("--input", help="The configuration file", default="configuration.json")
    parser.add_argument("--output", help="The folder to store the generated tests", default="./to_execute")
    args = parser.parse_args()
 
    logging.basicConfig(level=logging.WARNING)

    if not path.exists(args.input):
        logging.fatal(f"Cannot find the configuration file {args.input}.", file=sys.stderr)
        quit()

    if not path.isdir(args.output):
        logging.debug(f"Creating {args.output}, since it does not exist.")
        os.makedirs(args.output)

    with open(args.input, "r") as f:
        configuration = json.load(f)["Configuration"]

    path_to_templates = path.abspath("./templates")
    path_to_drivers = path.abspath("./drivers")
    
    test_id = str(uuid.uuid4())
    path_to_temp = path.join(path_to_drivers, "tmp")
    logging.info(f"Generating a test with the id {test_id} in {path_to_temp}.")    
    
    if path.isdir(path_to_temp):
        shutil.rmtree(path_to_temp)

    logging.debug(f"Creating new driver, based on the templates in {path_to_templates}.")
    shutil.copytree(path.join(path_to_templates, "faban", "driver", "ecsa"), path_to_temp)
    shutil.copyfile(path.join(path_to_templates, "deployment_descriptor", "template", "docker-compose.yml"), path.join(path_to_temp, "deploy", "docker-compose.yml"))
    
    replacements = []
    for entry in configuration:
	    replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configuration[entry]})
    replacements.append({"search_for": "${TEST_NAME}", "replace_with": test_id})

    logging.debug(f"Replacing values...")
    replace_values_in_file(path.join(path_to_temp, "build.properties"), replacements)
    replace_values_in_file(path.join(path_to_temp, "deploy", "run.xml"), replacements)
    shutil.copyfile(path.join(path_to_temp, "deploy", "run.xml"), path.join(path_to_temp, "config", "run.xml"))
    replace_values_in_file(path.join(path_to_temp, "src", "ecsa", "driver", "WebDriver.java"), replacements)
    replace_values_in_file(path.join(path_to_temp, "deploy", "docker-compose.yml"), replacements)
    
    logging.info("Compiling the Faban driver")
    current_folder = os.getcwd()
    os.chdir(path_to_temp)
    command = "ant deploy.jar -q"
    result = os.system(command)
    os.chdir(current_folder)

    if result != 0:
        logging.fatal(f"Could not compile test in {path_to_temp}.", file=sys.stderr)
        quit()

    path_to_output = path.join(path.abspath(args.output), test_id)
    logging.debug(f"Writing the test case into {path_to_output}...")   
    
    os.makedirs(path_to_output)
    shutil.copyfile(path.join(path_to_temp, "build", f"{test_id}.jar"), path.join(path_to_output, f"{test_id}.jar"))
    shutil.copyfile(path.join(path_to_temp, "config", "run.xml"), path.join(path_to_output, "run.xml"))
    shutil.copyfile(path.join(path_to_temp, "deploy", "docker-compose.yml"), path.join(path_to_output, "docker-compose.yml"))
    shutil.move(path_to_temp, path.join(path_to_drivers, test_id))
    
if __name__ == "__main__":
    generate_test()
