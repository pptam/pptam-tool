#!/usr/bin/env python

import os
import shutil
import json
import argparse
import logging
import uuid
from datetime import datetime
from os import path
from lib import *
from ini2json import covertIni2Json
from createTestConfigurationInterfaceHandler import deploymentHandler 
from createTestConfigurationInterfaceHandler import executionAndMeasurementHandler 
from createTestConfigurationInterfaceHandler import sutHandler 

# From configurationDictionary get all files (["file_to_change"]) and place holders.
# Copy files into destinationFolder.
# In every file (in destinationFolder), search for those place holders and replace them.
def copyAndReplacePlaceHoldersinFiles(destinationFolder, configurationDictionary, testID):
    replacements = []

    # Get place holders
    for entry in configurationDictionary:
        if(entry=="file_to_change"):
            continue
        if(entry=="test_name"):
            # Get lower case and upper case versions of place holders to replace.
            replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": testID})
            replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": testID})
            continue
            
        # Get lower case and upper case versions of place holders to replace.
        replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configurationDictionary[entry]})
        replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": configurationDictionary[entry]})
    

    # Get all files to replace
    filesList = configurationDictionary["file_to_change"]
    filesStr = ""
    for char in filesList:  
        filesStr += char 
    for f in filesStr.split(','):
        # Copy file into destinationFolder
        shutil.copyfile(path.join(f), path.join(destinationFolder, os.path.basename(f)))
        logging.debug("Replacing values in "+path.join(destinationFolder, os.path.basename(f))+".")
        replace_values_in_file(path.join(destinationFolder, os.path.basename(f)), replacements)
        
        
# Create a folder for a new test.
# Get from the configuration all the files that need to be changed, and copy them into the folder for the new test (drivers/tmp/test_id).
# Read from the configuration all place holders and updated them in the files.
# Handle the organisation of files and folders in the newly created drivers/testID (specific to each configuration).
# Remove drivers/tmp
# Copy the content of the drivers/testID into to_execute
def create_test(configuration_file_path, configuration_entries_to_overwrite):
    
    ##################################################################################################
    ## Generic part for every test ###################################################################
    ##################################################################################################
    
    # Load configuration.
    if not path.exists(configuration_file_path):
        logging.fatal(f"Cannot find the configuration file {configuration_file_path}.")
        quit()
    configuration = None
    with open(configuration_file_path, "r") as f:
        configuration = json.load(f)["Configuration"]
    
    # Generate random test ID.
    now = datetime.now()
    test_id = configuration["test_case_prefix"] + "-" + \
        now.strftime("%Y%m%d%H%M%S") + "-" + str(uuid.uuid4())[:8]
        
    # Create a temporary folder for the new test.
    path_to_drivers = path.abspath("./drivers")
    path_to_temp = path.join(path_to_drivers, "tmp")
    # Delete temporary files
    if path.isdir(path_to_temp):
        shutil.rmtree(path_to_temp)
    path_to_temp_id = path.join(path_to_temp, test_id)  
        
    if not path.isdir(path_to_temp):
        os.makedirs(path_to_temp)
    if not path.isdir(path_to_temp_id):
        os.makedirs(path_to_temp_id)
    else:
        print(f"{path_to_temp_id} is not empty. EXIT.")
        return        
    
    # If it does not exist, create output folder where a fully generated test will be placed.
    output = configuration["test_case_creation_folder"]
    if not path.isdir(output):
        logging.debug(f"Creating {output}, since it does not exist.")
        os.makedirs(output)



    # Get files that contain place holders that need to be replaced.
    deploymentOpt = configuration["deployment"] 
    executionAndMeasurementOpt = configuration["execution_and_measurement"]
    sutOpt = configuration["sut"]
    
    # Handle deployment place holders.
    deploymentConf = None
    with open("../configuration/thirdParty/deployment.json", "r") as f:
        deploymentConf = json.load(f)[deploymentOpt]
        # Replace all files with place holders.
        copyAndReplacePlaceHoldersinFiles(path_to_temp_id, deploymentConf, test_id)
        
    # Handle execution and measurement place holders.
    executionAndMeasurementConf = None
    with open("../configuration/thirdParty/executionAndMeasurement.json", "r") as f:
        executionAndMeasurementConf = json.load(f)[executionAndMeasurementOpt]
        # Replace all files with place holders.
        copyAndReplacePlaceHoldersinFiles(path_to_temp_id, executionAndMeasurementConf, test_id)
    
    # Handle system under test place holders.
    sutConf = None
    with open("../configuration/thirdParty/sut.json", "r") as f:
        sutConf = json.load(f)[sutOpt]
        # Replace all files with place holders.
        copyAndReplacePlaceHoldersinFiles(path_to_temp_id, sutConf, test_id) 
    
    # Get the test plan. Update the test files. Create tests. 
    #with open("../configuration/thirdParty/deployment.json", "r") as f:
        #deploymentConf = json.load(f)[deploymentOpt]
    ##################################################################################################
        
        
        
        
    ##################################################################################################
    ## Handle specific test configuration ############################################################
    ##################################################################################################
    deploymentHandler(test_id, deploymentOpt, deploymentConf)
    executionAndMeasurementHandler(test_id, executionAndMeasurementOpt, executionAndMeasurementConf)
    sutHandler(test_id, sutOpt, sutConf)
    ##################################################################################################
        
        
        
        
    ##################################################################################################
    ## Generic part for every test ###################################################################
    ##################################################################################################
    if not path.isdir(output):
        logging.debug(f"Creating {output}, since it does not exist.")
        os.makedirs(output)

    path_to_output = path.join(path.abspath(output), test_id)
    logging.info(f"Writing the test case into {path_to_output}.")

    os.makedirs(path_to_output)
    shutil.copyfile(path.join(path_to_temp, "build", f"{test_id}.jar"), path.join(path_to_output, f"{test_id}.jar"))
    shutil.copyfile(path.join(path_to_temp, "config", "run.xml"), path.join(path_to_output, "run.xml"))
    shutil.copyfile(path.join(path_to_temp, "deploy", "docker-compose.yml"), path.join(path_to_output, "docker-compose.yml"))
    shutil.move(path_to_temp, path.join(path_to_drivers, test_id))
    logging.info(f"Done.")
    
    return test_id
    ##################################################################################################

def generateTestCampaign(test_id, folder, testCampaignConfWithMetricConfGenerated, executionAndMeasurementOpt):
    testCampaignConfWithMetricConfGeneratedPath = path.join(folder, testCampaignConfWithMetricConfGenerated)

    # If file does not exist, add the new metric at the top of the file, and populate it with all the existing tests to execute.
    if not os.path.isfile(testCampaignConfWithMetricConfGeneratedPath):
        with open(path.join(testCampaignConfWithMetricConfGeneratedPath), "w") as fTest:
            # Write metric header.
            print("Write metric header.")
            with open(path.join(folder, "measurementMetricTemplate.json"), "r") as f:
                measurementMetricTemplate = json.load(f)[executionAndMeasurementOpt]
                for key in measurementMetricTemplate.keys():
                    if(key=="metric_measurement_id"):
                        fTest.write(f"[{measurementMetricTemplate[key]}]")
                        fTest.write("\n")
                        continue
                    fTest.write(key+"="+measurementMetricTemplate[key])
                    fTest.write("\n")
                fTest.write("\n")
            # Write other tests.
            for testId in os.scandir(path.join("./to_execute")):
                    if (path.isdir(testId)):
                        fTest.write("[Test_"+testId.name+"]\n")
                        fTest.write("test_id="+str(testId.name))
                        with open(path.join(folder, "testCampaignTemplate.json"), "r") as f:
                            testCampaignTemplate = json.load(f)["TestCampaign"]
                            for key in testCampaignTemplate.keys():
                                fTest.write("\n")
                                fTest.write(key+"="+testCampaignTemplate[key])
                            fTest.write("\n")
                            fTest.write("\n")
    else:
        #print("Path does exist.")
        # Otherwise, add the new test to the bottom.
        with open(path.join(folder, testCampaignConfWithMetricConfGenerated), "a") as fTest:
            fTest.write("\n")
            fTest.write("[Test_"+test_id+"]\n")
            fTest.write("test_id="+test_id)
            with open(path.join(folder, "testCampaignTemplate.json"), "r") as f:
                testCampaignTemplate = json.load(f)["TestCampaign"]
                for key in testCampaignTemplate.keys():
                    fTest.write("\n")
                    fTest.write(key+"="+testCampaignTemplate[key])
    testCampaignConfWithMetricConfGenerated = "../configuration/"+testCampaignConfWithMetricConfGenerated
    covertIni2Json(testCampaignConfWithMetricConfGenerated, "../configuration/testCampaignConfWithMetricConfGenerated.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates test cases.")
    parser.add_argument("--configuration", metavar="path_to_configuration_file", help="Configuration file", default="../configuration/configuration.json")
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)
    parser.add_argument("--overwrite", help="Configuration values, which overwrite the values in the configuration file. Format: name1=value1 name2=value2 ...", metavar="key=value", nargs="+", default=[])
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    test_id = create_test(args.configuration, args.overwrite)
    # Generate test campaign configuration files.
    folder = path.abspath("../configuration/")
    #print("folder="+folder)
    testCampaignConfWithMetricConfGenerated = "testCampaignConfWithMetricConfGenerated.ini"
    logging.info(f"Generate "+testCampaignConfWithMetricConfGenerated+".")
    
    # Get current execution and measurement option.
    executionAndMeasurementOpt = ""
    with open(args.configuration, "r") as f:
        configuration = json.load(f)["Configuration"]
        executionAndMeasurementOpt = configuration["execution_and_measurement"]
    
    generateTestCampaign(test_id, folder, testCampaignConfWithMetricConfGenerated, executionAndMeasurementOpt)
    logging.info(f"Done.")
