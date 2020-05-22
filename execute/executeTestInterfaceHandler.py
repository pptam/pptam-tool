# Specific handling of deployment and monitoring operations to tools that are executing these.
# Interface to separate tools.

from lib import *

def deploymentHandler(testFolder, test_id, deploymentOpt, deploymentConf):
    if(deploymentOpt=="DOCKER"):
        deploymendHandlerDocker(testFolder, test_id, deploymentConf)

# Based on execution and measurement type, calls a corresponding handler.   
# Returns run_id.     
def executionAndMeasurementHandler(test_id, executionAndMeasurementOpt, executionAndMeasurementConf):
    if(executionAndMeasurementOpt=="FABAN"):
        return executionAndMeasurementHandlerFaban(test_id, executionAndMeasurementConf)

# Based on execution and measurement type, calls a corresponding handler.        
def executionMonitoringHandler(test_id, run_id, executionMonitoringOpt, executionAndMeasurementConf):
    if(executionMonitoringOpt=="FABAN"):
        return executionMonitoringHandlerFaban(test_id, run_id, executionAndMeasurementConf)

# Based on execution and measurement type, calls a corresponding handler.        
def executionOutputHandler(test_id, run_id, test_output_path, executionAndMeasurementOpt, executionAndMeasurementConf):
    if(executionOutputOpt=="FABAN"):
        executionOutputHandlerFaban(test_id, run_id, test_output_path, executionAndMeasurementConf)
        
def executionCleanupHandler(test_id, cleanupOpt, deploymentConf):
    if(cleanupOpt=="DOCKER"):
        executionCleanupHandlerDocker(test_id, deploymentConf)
        


def deploymendHandlerDocker(testFolder, test_id, deploymentConf):
    deployment_descriptor = f"{testFolder}/{test_id}/docker-compose.yml"
    command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} {test_id}"
    
    run_external_applicaton(command_deploy_stack)
    
def executionAndMeasurementHandlerFaban(test_id, executionAndMeasurementConf):
    input = path.abspath(configuration["test_case_to_execute_folder"])
    faban_client = path.abspath("./faban/benchflow-faban-client/target/benchflow-faban-client.jar")
    faban_master = f"http://{executionAndMeasurementConf['faban_ip']}:9980/"
    temporary_file = f"{test_id}.tmp"
    
    driver = f"{input}/{test_id}/{test_id}.jar"
    driver_configuration = f"{input}/{test_id}/run.xml"
    
    command_deploy_faban = f"java -jar {faban_client} {faban_master} deploy {test_id} {driver} {driver_configuration} > {temporary_file}"
    
    with open(temporary_file, "r") as f:
        run_id = f.readline().rstrip()
        os.remove(temporary_file)
        return run_id

    run_external_applicaton(command_deploy_faban)

def executionMonitoringHandlerFaban(test_id, run_id, executionAndMeasurementConf):
    temporary_file = f"{test_id}.tmp"
    
    faban_client = path.abspath("./faban/benchflow-faban-client/target/benchflow-faban-client.jar")
    faban_master = f"http://{executionAndMeasurementConf['faban_ip']}:9980/"
    
    command_status_faban = f"java -jar {faban_client} {faban_master} status {run_id} > {temporary_file}"
            
    run_external_applicaton(command_status_faban)

    with open(temporary_file, "r") as f:
        std_out_status = f.readline().rstrip()
        os.remove(temporary_file)
        return std_out_status

def executionOutputHandlerFaban(test_id, run_id, test_output_path, executionAndMeasurementConf):
    os.makedirs(test_output_path)
    shutil.copytree(f"./faban/output/{run_id}", f"{test_output_path}/faban")
    shutil.move(f"{input}/{test_id}", f"{test_output_path}/definition")
    shutil.copyfile(configuration_file_path, f"{test_output_path}/configuration.json")

    faban_client = path.abspath("./faban/benchflow-faban-client/target/benchflow-faban-client.jar")
    faban_master = f"http://{executionAndMeasurementConf['faban_ip']}:9980/"

    command_info_faban = f"java -jar {faban_client} {faban_master} info {run_id} > {test_output_path}/faban/runInfo.txt"
    run_external_applicaton(command_info_faban)
    
def executionCleanupHandlerDocker(test_id, deploymentConf):
    command_undeploy_stack = f"docker stack rm {test_id}"
    run_external_applicaton(command_undeploy_stack, False)
    