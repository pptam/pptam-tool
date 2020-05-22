#!/usr/bin/env python

import os
import time
import argparse
import logging
from os import path
import json
from time import sleep
import subprocess
import shutil
from lib import *

from executeTestInterfaceHandler import deploymentHandler
from executeTestInterfaceHandler import executionAndMeasurementHandler
from executeTestInterfaceHandler import executionMonitoringHandler
from executeTestInterfaceHandler import executionOutputHandler
from executeTestInterfaceHandler import executionCleanupHandler

def getMeasurementMetric(measurementMetricID):
    pass

def execute_test(configuration_file_path, testCampaignConfWithMetricConfGeneratedFilePath):
    if not path.exists(configuration_file_path):
        logging.fatal(f"Cannot find the configuration file {configuration_file_path}.")
        raise RuntimeError

    with open(configuration_file_path, "r") as f:
        configuration = json.load(f)["Configuration"]

    input = path.abspath(configuration["test_case_to_execute_folder"])
    if not path.isdir(input):
        logging.fatal(f"Cannot find the test case folder {input}.")
        raise RuntimeError
    else:
        logging.debug(f"Executing test cases from {input}.")
        
        
    # Get files that contain place holders that need to be replaced.
    deploymentOpt = configuration["deployment"] 
    executionAndMeasurementOpt = configuration["execution_and_measurement"]
    sutOpt = configuration["sut"]
    
    # Handle deployment place holders.
    deploymentConf = None
    with open("../configuration/thirdParty/deployment.json", "r") as f:
        deploymentConf = json.load(f)[deploymentOpt]
        
    # Handle execution and measurement place holders.
    executionAndMeasurementConf = None
    with open("../configuration/thirdParty/executionAndMeasurement.json", "r") as f:
        executionAndMeasurementConf = json.load(f)[executionAndMeasurementOpt]
    
    # Handle system under test place holders.
    sutConf = None
    with open("../configuration/thirdParty/sut.json", "r") as f:
        sutConf = json.load(f)[sutOpt]
   

    seconds_to_wait_for_deployment = int(configuration["test_case_waiting_for_deployment_in_seconds"])
    seconds_to_wait_for_undeployment = int(configuration["test_case_waiting_for_undeployment_in_seconds"])
    time_to_complete_one_test = seconds_to_wait_for_deployment + seconds_to_wait_for_undeployment + (((int(configuration["test_case_ramp_up_in_seconds"]) + int(configuration["test_case_steady_state_in_seconds"]) + int(configuration["test_case_ramp_down_in_seconds"])) // 60) + 1) * 60
    time_to_complete_all_tests = (len([name for name in os.listdir(f"{input}/") if os.path.isdir(f"{input}/{name}")]) * time_to_complete_one_test // 60) + 1
    logging.info(f"Estimated duration of ONE test: approx. {time_to_complete_one_test} seconds.")
    logging.info(f"Estimated duration of ALL tests: approx. {time_to_complete_all_tests} minutes.")

    output = path.abspath(configuration["test_case_executed_folder"])
    logging.debug(f"Storing results in {output}.")

    command_to_execute_before_a_test = configuration["pre_exec_external_command"]
    command_to_execute_after_a_test = configuration["post_exec_external_command"]
    command_to_execute_at_a_test = configuration["on_exec_external_command"]
    #sut_ip = configuration["sut_ip"]
    #sut_port = configuration["sut_port"]

    #for f in os.scandir(input):
        #if (path.isdir(f)):
        
    # Load test campaign conf.
    with open(testCampaignConfWithMetricConfGeneratedFilePath, "r") as f:
        testCampaignConfWithMetricConfGenerated = json.load(f)
        for category in testCampaignConfWithMetricConfGenerated:
            if category.startswith("Test_"):
                if(testCampaignConfWithMetricConfGenerated[category]["test_enabled"] == "TRUE"):
                    number_of_executions = int(testCampaignConfWithMetricConfGenerated[category]["number_of_executions"])
                    while(number_of_executions>0):
                        number_of_executions = number_of_executions-1
                        try:
                            logging.info(f"Executing test case {f.name}.")
            
                            if (len(command_to_execute_before_a_test) > 0):
                                #run_external_applicaton(f"{command_to_execute_before_a_test} {sut_ip} {sut_port}")
                                run_external_applicaton(f"{command_to_execute_before_a_test}")
            
                            # test_id = f.name
                            test_id = testCampaignConfWithMetricConfGenerated[category]["test_id"]
                            temporary_file = f"{test_id}.tmp"
            
                            test_output_path = f"{output}/{test_id}"
                            if path.isdir(test_output_path):
                                logging.info(f"Removing path {test_output_path} since it already exists.")
                                shutil.rmtree(path, ignore_errors=False, onerror=RuntimeError)
            
                            ##################################################################################################
                            ## Handle specific execution commands ############################################################
                            ##################################################################################################
                            deploymentHandler(input, test_id, deploymentOpt, deploymentConf)
                            ##################################################################################################

                            logging.debug(f"Waiting for {seconds_to_wait_for_deployment} seconds.")
                            wait(seconds_to_wait_for_deployment, time_to_complete_one_test, "Waiting for deployment.", 0)
                            time_elapsed = seconds_to_wait_for_deployment
                            
                            ##################################################################################################
                            ## Handle specific execution commands ############################################################
                            ##################################################################################################
                            run_id = executionAndMeasurementHandler(test_id, executionAndMeasurementOpt, executionAndMeasurementConf)
                            ##################################################################################################                          

                            logging.debug(f"Obtained {run_id} as run ID.")
            
                            status = ""
                            external_tool_was_started = False
            
                            while ((status != "COMPLETED") and (status != "FAILED")):
                                ##################################################################################################
                                ## Handle specific monitoring commands ###########################################################
                                ##################################################################################################
                                status = executionMonitoringHandler(test_id, run_id, executionAndMeasurementOpt, executionAndMeasurementConf)
                                ##################################################################################################
                              
                                logging.debug(f"Current test execution status: {status}.")
            
                                if (status == "STARTED" and external_tool_was_started == False and len(command_to_execute_before_a_test) > 0):
                                    external_tool_was_started = True
                                    #run_external_applicaton(f"{command_to_execute_at_a_test} {sut_ip} {sut_port}")
                                    run_external_applicaton(f"{command_to_execute_at_a_test}")
            
                                if ((status != "COMPLETED") and (status != "FAILED")):
                                    if time_elapsed < time_to_complete_one_test:
                                        wait_until = 60
                                    else:
                                        wait_until = 10
            
                                    logging.debug(f"Waiting for {wait_until} seconds.")
                                    wait(wait_until, time_to_complete_one_test, "Waiting for test to finish.", time_elapsed, time_to_complete_one_test - seconds_to_wait_for_undeployment)
                                    time_elapsed += wait_until
            
                            if (len(command_to_execute_after_a_test) > 0):
                                #run_external_applicaton(f"{command_to_execute_after_a_test} {sut_ip} {sut_port}")
                                run_external_applicaton(f"{command_to_execute_after_a_test}")
                        finally:
                            ##################################################################################################
                            ## Handle specific execution output commands #####################################################
                            ##################################################################################################
                            executionCleanupHandler(test_id, deploymentOpt, deploymentConf)
                            ##################################################################################################
                                        
                            if path.isfile(temporary_file):
                                os.remove(temporary_file)
            
                        if (status == "COMPLETED"):
                            logging.debug(f"Waiting for {seconds_to_wait_for_undeployment} seconds.")
                            wait(seconds_to_wait_for_undeployment, time_to_complete_one_test, "Waiting for undeployment.  ", time_elapsed)
                            progress(time_to_complete_one_test, time_to_complete_one_test, "Done.                      \n")
                            
                            ##################################################################################################
                            ## Handle specific execution output commands #####################################################
                            ##################################################################################################
                            executionOutputHandler(test_id, run_id, test_output_path, executionAndMeasurementOpt, executionAndMeasurementConf)
                            ##################################################################################################

                            logging.info(f"Test {test_id} completed. Test results can be found in {test_output_path}.")
                        else:
                            progress(time_to_complete_one_test, time_to_complete_one_test, "Failed.                    \n")
                            logging.fatal(f"Test {test_id} with run id {run_id} failed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("--configuration", metavar="path_to_configuration_file", help="Configuration file", default="../configuration/configuration.json")
    parser.add_argument("--testCampaign", metavar="path_to_test_campaign_configuration_file", help="Test campaign and metric configuration file", default="../configuration/testCampaignConfWithMetricConfGenerated.json")
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    print("args.configuration="+args.testCampaign)
    execute_test(args.configuration, args.testCampaign)
