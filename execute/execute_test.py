#!/usr/bin/env python3.7

import os
import time
import argparse
import logging
from os import path
import json
import sys
from time import sleep
import subprocess

def wait(seconds):
    while seconds > 0:
        sys.stdout.write(f"Waiting for {seconds}...     \r")
        seconds -= 1
        sleep(1)

def execute_test(configuration_file_path):
    if not path.exists(configuration_file_path):
        logging.fatal(f"Cannot find the configuration file {configuration_file_path}.")
        quit()

    with open(configuration_file_path, "r") as f:
        configuration = json.load(f)["Configuration"]

    input = configuration["test_case_to_execute_folder"]
    if not path.isdir(input):
        logging.fatal(f"Cannot find the test case folder {input}.")
        quit()
    else:
        input = path.abspath(input)
        logging.debug(f"Executing test cases from {input}.")

    output = configuration["test_case_executed_folder"]
    if not path.isdir(input):
        logging.fatal(f"Cannot find the results folder {output}.")
        quit()
    else:
        output = path.abspath(output)
        logging.debug(f"Storing results in {output}.")
        
    faban_master = f"http://{configuration['faban_ip']}:9980/"
    faban_client = "./faban/benchflow-faban-client/target/benchflow-faban-client.jar"

    command_to_execute_before_a_test = configuration["pre_exec_external_command"]
    command_to_execute_after_a_test = configuration["post_exec_external_command"]
    seconds_to_wait_for_deployment = int(configuration["test_case_waiting_for_deployment_in_seconds"])

    for f in os.scandir(input):
        if (path.isdir(f)):
            try:
                logging.info(f"Executing test case {f.name}.")
                
                logging.debug(f"Executing {command_to_execute_before_a_test}.")
                result_before = os.system(command_to_execute_before_a_test)
                if result_before != 0:
                    logging.fatal(f"Could not execute {command_to_execute_before_a_test}.")
                    quit()

                test_id = f.name
                command_deploy_stack = f"docker stack deploy --compose-file={f.path}/docker-compose.yml {test_id}"
                
                logging.debug("Deploying the system under test.")
                result_deploy_stack = os.system(command_deploy_stack)
                if result_deploy_stack != 0:
                    logging.fatal(f"Could not deploy the system under test for test {test_id}.")       
                    raise RuntimeError                    

                wait(seconds_to_wait_for_deployment)

                driver = f"{input}/{test_id}/{test_id}.jar"
                driver_configuration = f"{input}/{test_id}/run.xml"
                deployment_descriptor = f"{input}/{test_id}/docker-compose.yml"

                command_deploy_faban = f"java -jar {faban_client} {faban_master} deploy {test_id} {driver} {driver_configuration}"
                print(command_deploy_faban)

                logging.debug("Deploying the load driver")

                process_deploy_faban = subprocess.run(command_deploy_faban.split(" "), shell=True, stdout=subprocess.PIPE)
                result_deploy_faban = process_deploy_faban.communicate()
                print(result_deploy_faban.stdout.decode('utf-8'))

            finally:
                command_undeploy_stack = f"docker stack rm {test_id}"
                result_undeploy_stack = os.system(command_undeploy_stack)
                if result_undeploy_stack != 0:
                    logging.fatal(f"Could not undeploy the system under test for test {test_id}.")
                quit()

        #     RUN_ID = ""
        #     readFromFile = ReadFromFile(RUN_ID_FILE)
        #     for line in readFromFile.readLines():
        #         RUN_ID = readFromFile.readLines()

        #     print("RUN_ID=" + RUN_ID)

        #     # Cleanup
        #     commonMethods.removeFileRelativePath(
        #         self.rootDirectory + "/" + RUN_ID_FILE)

        #     print("Run ID: " + RUN_ID)

        #     # Wait for the test to be done.
        #     STATUS = ""

        #     while ((STATUS != "COMPLETED") and (STATUS != "FAILED")):
        #         STATUS_FILE = "STATUS.txt"

        #         # Get test status
        #         # java -jar ./faban/benchflow-faban-client/target/benchflow-faban-client.jar $FABAN_MASTER status $RUN_ID | (read STATUS ; echo $STATUS > STATUS.txt)
        #         terminalCmd = "java -jar " + testExecutorDestination + "/faban/benchflow-faban-client/target/benchflow-faban-client.jar " + \
        #             FABAN_MASTER + " status " + RUN_ID + \
        #             " | (read STATUS ; echo $STATUS > " + STATUS_FILE + ")"
        #         print("To execute: " + terminalCmd)
        #         os.system(terminalCmd)

        #         readFromFile = ReadFromFile(STATUS_FILE)
        #         for line in readFromFile.readLines():
        #             STATUS = readFromFile.readLines()

        #         # TODO: Comment out
        #         #STATUS = "COMPLETED"
        #         print("Current STATUS: " + STATUS)

        #         # Only used for testing with Mirai
        #         # TODO: Not sure how these should work.
        #         # if (STATUS != "STARTED"):
        #         # duration=$SECONDS
        #         # echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
        #         # if [ $MIRAI_STARTED -eq 0 ]
        #         # if [ $SECONDS -gt 180 ]
        #         # MIRAI_STARTED=1
        #         # pass

        #         # cleanup
        #         commonMethods.removeFileRelativePath(
        #             self.rootDirectory + "/" + STATUS_FILE)
        #         # TODO: Uncomment
        #         time.sleep(120)

        #     # Stop the resource data collection and store the data
        #     # echo "Data collection: "
        #     # curl http://$SUT_IP:$STAT_COLLECTOR_PORT/stop
        #     # echo ""

        #     # Execute commands after a test.
        #     for postExec in pptamConfigurationData.getPostExecExternalCommands():
        #         print("")
        #         print("------------------------------------")
        #         print("    --- Execute external command ---")
        #         os.system(postExec)
        #         print("------------------------------------")
        #         print("")

        #     print("Undeploying the system under test")
        #     # undeploy the system under test

        #     #terminalCmd = "cd "+self.rootDirectory+"/to_execute/"+testID
        #     # os.system(terminalCmd)
        #     # cd ./to_execute/$TEST_ID/

        #     # undeploy the system under test
        #     terminalCmd = "docker stack rm " + testFolder + "/" + testID + "/" + testID
        #     print("To execute: " + terminalCmd)
        #     os.system(terminalCmd)

        #     # be sure everything is clean
        #     terminalCmd = "docker stack rm $(docker stack ls --format \"{{.Name}}\") || true"
        #     print("To execute: " + terminalCmd)
        #     os.system(terminalCmd)
        #     terminalCmd = "docker rm -f -v $(docker ps -a -q) || true"
        #     os.system(terminalCmd)

        #     # saving test results
        #     print("Saving test results")
        #     os.mkdir(executedTests + "/" + testID)
        #     os.mkdir(executedTests + "/" + testID + "/faban")

        #     terminalCmd = "java -jar " + testExecutorDestination + "/faban/benchflow-faban-client/target/benchflow-faban-client.jar " + \
        #         FABAN_MASTER + " info " + RUN_ID + " > " + executedTests + "/" + testID + "/faban/runInfo.txt"
        #     print("To execute: " + terminalCmd)
        #     os.system(terminalCmd)

        #     fileOriginAbsPath = testExecutorDestination + \
        #         "/faban/output/" + RUN_ID + "summary.xml"
        #     folderTargetAbsPath = executedTests + "/" + testID + "/faban/"
        #     if path.isdir(folderTargetAbsPath) == False:
        #         os.mkdir(folderTargetAbsPath)
        #     commonMethods.copyFile(fileOriginAbsPath, folderTargetAbsPath)

        #     fileOriginAbsPath = testExecutorDestination + \
        #         "/faban/output/" + RUN_ID + "summary.xml"
        #     folderTargetAbsPath = executedTests + "/" + testID + "/faban/"
        #     if path.isdir(folderTargetAbsPath) == False:
        #         os.mkdir(folderTargetAbsPath)
        #     commonMethods.copyFileRel(
        #         fileOriginAbsPath, folderTargetAbsPath)

        #     fileOriginAbsPath = testExecutorDestination + "/faban/output/" + RUN_ID + "log.xml"
        #     folderTargetAbsPath = executedTests + "/" + testID + "/faban/"
        #     if path.isdir(folderTargetAbsPath) == False:
        #         os.mkdir(folderTargetAbsPath)
        #     commonMethods.copyFileRel(
        #         fileOriginAbsPath, folderTargetAbsPath)
        #     # mkdir -p ./executed/$TEST_ID/stats
        #     # curl http://$SUT_IP:$STAT_COLLECTOR_PORT/data > executed/$TEST_ID/stats/cpu.txt
        #     # cp ./services/stats/cpu.txt ./executed/$TEST_ID/stats/cpu.txt
        #     folderOriginAbsPath = testExecutorDestination + "/to_execute/" + testID + "/"
        #     folderTargetAbsPath = executedTests + "/" + testID + "/definition"
        #     if path.isdir(folderTargetAbsPath) == False:
        #         os.mkdir(folderTargetAbsPath)
        #     commonMethods.moveFromFolder2Folder(
        #         folderOriginAbsPath, folderTargetAbsPath)

            
            quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executes test cases.")
    parser.add_argument("--configuration", metavar="path_to_configuration_file", help="Configuration file", default="configuration.json")    
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)    
    args = parser.parse_args()
 
    logging.basicConfig(format='%(message)s', level=args.logging * 10)   
    execute_test(args.configuration)
