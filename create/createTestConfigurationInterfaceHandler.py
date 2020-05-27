from os import path
import logging
import os
import shutil
import distutils.dir_util
from distutils.dir_util import copy_tree

##########################################################################################
# Handles operations related to creation of tests.
##########################################################################################

# Based on deployment type, calls a corresponding handler.
def deploymentHandler(test_id, deploymentOpt, deploymentConf):
    if(deploymentOpt=="DOCKER"):
        deploymendHandlerDocker(test_id, deploymentConf)

# Based on execution and measurement type, calls a corresponding handler.        
def executionAndMeasurementHandler(test_id, executionAndMeasurementOpt, executionAndMeasurementConf):
    if(executionAndMeasurementOpt=="FABAN"):
        executionAndMeasurementHandlerFaban(test_id, executionAndMeasurementConf)

# Based on SUT type, calls a corresponding handler.
def sutHandler(test_id, sutOpt, sutConf):
    if(sutOpt=="SOCKS2"):
        sutHandlerSocks2(test_id, sutConf)
    elif(sutOpt=="TRAIN_TICKET"):
        sutHandlerTrainTicket(test_id, sutConf)
        
def deploymendHandlerDocker(test_id, deploymentConf):
    pass


def executionAndMeasurementHandlerFaban(test_id, executionAndMeasurementConf):
    path_to_templates = path.abspath("./templates")
    path_to_drivers = path.abspath("./drivers")
    path_to_temp = path.join(path_to_drivers, "tmp/")

    logging.debug(f"Generating a test with the id {test_id} in {path_to_temp}.")

    logging.debug(f"Creating new driver, based on the templates in {path_to_templates}.")  
    #shutil.copytree(path.join(path_to_templates, "faban", "driver", "ecsa"), path_to_temp)

    # Seems to be a bug in distutils. If you copy folder, then remove it, then copy again it will fail, because it caches all the created dirs. To workaround you can clear _path_created before copy
    # https://stackoverflow.com/questions/9160227/dir-util-copy-tree-fails-after-shutil-rmtree/28055993
    distutils.dir_util._path_created = {}
    
    copy_tree(path.join(path_to_templates, "faban", "driver", "ecsa"), path_to_temp)
    shutil.copyfile(path.join(path_to_templates, "deployment_descriptor", "template", "docker-compose.yml"), path.join(path_to_temp, "deploy", "docker-compose.yml"))
    
    #replacements = []
    #for entry in configuration:
    #    replacements.append({"search_for": "${" + entry.upper() + "}", "replace_with": configuration[entry]})
    #    replacements.append({"search_for": "${" + entry.lower() + "}", "replace_with": configuration[entry]})

    #replacements.append({"search_for": "${TEST_NAME}", "replace_with": test_id})

    #logging.debug(f"Replacing values.")
    #replace_values_in_file(path.join(path_to_temp, "build.properties"), replacements)
    #replace_values_in_file(path.join(path_to_temp, "deploy", "run.xml"), replacements)
    #shutil.copyfile(path.join(path_to_temp, "deploy", "run.xml"), path.join(path_to_temp, "config", "run.xml"))
    #replace_values_in_file(path.join(path_to_temp, "src", "ecsa", "driver", "WebDriver.java"), replacements)
    #replace_values_in_file(path.join(path_to_temp, "deploy", "docker-compose.yml"), replacements)
    
    # Copy files with replaced place holders to corresponding folders.
    shutil.move(path.join(path_to_temp, test_id, "build.properties"), path.join(path_to_temp, "build.properties"))
    shutil.copy(path.join(path_to_temp, test_id, "run.xml"), path.join(path_to_temp, "deploy", "run.xml"))
    shutil.move(path.join(path_to_temp, test_id, "run.xml"), path.join(path_to_temp, "config", "run.xml"))
    shutil.move(path.join(path_to_temp, test_id, "WebDriver.java"), path.join(path_to_temp, "src", "ecsa", "driver", "WebDriver.java"))
    shutil.move(path.join(path_to_temp, test_id, "docker-compose.yml"), path.join(path_to_temp, "deploy", "docker-compose.yml"))
    shutil.move(path.join(path_to_temp, test_id, "build.xml"), path.join(path_to_temp, "build.xml"))
    
    # Remove test temporary file
    if path.isdir(path.join(path_to_temp, test_id)):
        logging.debug(f"Delete "+path.join(path_to_temp, test_id)+".")
        shutil.rmtree(path.join(path_to_temp, test_id))
    
    logging.debug("Compiling the Faban driver")
    current_folder = os.getcwd()
    os.chdir(path_to_temp)
    command = "ant deploy.jar -q -S"
    result = os.system(command)
    os.chdir(current_folder)

    if result != 0:
        logging.fatal(f"Could not compile test in {path_to_temp}.")
        quit()
        
def sutHandlerSocks2(test_id, sutConf):
        pass
    
def sutHandlerTrainTicket(test_id, sutConf):
        pass