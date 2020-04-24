import os
import os.path
from os import path
import time

from configurationParser.ReadFromFile import ReadFromFile
from configurationParser.WriteToFile import WriteToFile
from configurationParser.CommonMethods import CommonMethods

# Manage the execution of the tests

class TestExecutor: 
    rootDirectory = None
    parseConfiguration = None
    # Constructor.
    def __init__(self, root, configurationData): 
        self.rootDirectory = root
        self.parseConfiguration = configurationData
    
        # Create folder with relative path.
    def executeTests(self, testExecutorDestination):
        systemConfigurationData = self.parseConfiguration.getSystemConfigurationData()
        pptamConfigurationData = systemConfigurationData.getPPTAMConfigurationData()
        fabanConfigurationData = systemConfigurationData.getFabanConfigurationData()
        dockerConfigurationData = systemConfigurationData.getDockerConfigurationData()
        
        commonMethods = CommonMethods()
        
        # Check the folder for the future executed tests.
        # Make it clean.
        executedTests = testExecutorDestination+"/to_execute/executed"
        print("Store executed tests in: "+executedTests)
        if path.isdir(executedTests):
            print("Clean folder "+executedTests)
            commonMethods.deleteFilesFromFolder(executedTests)
        else:
            os.mkdir(executedTests)

        FABAN_IP = pptamConfigurationData.getFabanIP()
        FABAN_IP = FABAN_IP.replace(" ", "")
        print("FABAN_IP="+FABAN_IP)
        #FABAN_IP=$(getProperty "faban.ip")
        FABAN_MASTER = "http://"+pptamConfigurationData.getFabanIP()+":"+pptamConfigurationData.getSutPort()+"/"
        FABAN_MASTER = FABAN_MASTER.replace(" ", "")
        print("FABAN_MASTER="+FABAN_MASTER)
        #FABAN_MASTER="http://$FABAN_IP:9980/";
        # TODO: should we configure FABAN_CLIENT externally?
        FABAN_CLIENT="./faban/benchflow-faban-client/target/benchflow-faban-client.jar"
        SUT_IP=pptamConfigurationData.getSutIP()
        #SUT_IP=$(getProperty "sut.ip")
        #STAT_COLLECTOR_PORT=$(getProperty "stat.collector.port")
        
        # Get all test folders - test IDs.
        testFolder = testExecutorDestination+"/to_execute"
        print("Execute tests from "+testFolder)
        for f in os.scandir(testFolder):
            # Execute commands before a test.
            for preExec in pptamConfigurationData.getPreExecExternalCommands():
                print("")
                print("------------------------------------")
                print("    --- Execute external command ---")
                os.system(preExec)
                print("------------------------------------")
                print("")
                
            if f.is_dir():
                testID = f.name
                print("")
                print("Starting test: "+testID)
                print("Deploying the system under test")
                
                #terminalCmd = "cd ./to_execute/"+testID 
                #os.system(terminalCmd)
                terminalCmd = "docker stack deploy --compose-file=docker-compose.yml "+testFolder+"/"+testID 
                print("To execute: "+terminalCmd)
                os.system(terminalCmd)
                
                print("Waiting for the system to be ready")
                # TODO: Uncomment/uncomment not to wait for too long
                time.sleep(120)
                #terminalCmd = "sleep 120"
                #os.system(terminalCmd)
                
                terminalCmd = "export "+testFolder+"/"+testID 
                print("To execute: "+terminalCmd)
                os.system(terminalCmd)
                
                test_name=testID
                driver="to_execute/"+testID+"/"+testID+".jar"
                driver_conf="to_execute/"+testID+"/run.xml"
                deployment_descriptor="to_execute/"+testID+"/docker-compose.yml"
                
                print("Deploying the load driver")
                # Deploy and start the test
                RUN_ID_FILE = "RUN_ID.txt"
                terminalCmd = "java -jar "+FABAN_CLIENT+" "+FABAN_MASTER+" deploy "+test_name+" "+driver+" "+driver_conf+" | (read RUN_ID ; echo $RUN_ID > "+RUN_ID_FILE+")"
                os.system(terminalCmd)
                
                RUN_ID = ""
                readFromFile = ReadFromFile(RUN_ID_FILE)
                for line in readFromFile.readLines():
                    RUN_ID = readFromFile.readLines()
                
                print("RUN_ID="+RUN_ID)
                
                # Cleanup
                commonMethods.removeFileRelativePath(self.rootDirectory+"/"+RUN_ID_FILE)
                
                print("Run ID: "+RUN_ID)
                
                # Wait for the test to be done.
                STATUS=""
                
                while ( (STATUS != "COMPLETED") and (STATUS != "FAILED")):
                    STATUS_FILE = "STATUS.txt"
                 
                    # Get test status
                    #java -jar ./faban/benchflow-faban-client/target/benchflow-faban-client.jar $FABAN_MASTER status $RUN_ID | (read STATUS ; echo $STATUS > STATUS.txt)
                    terminalCmd = "java -jar "+testExecutorDestination+"/faban/benchflow-faban-client/target/benchflow-faban-client.jar "+FABAN_MASTER+" status "+RUN_ID+" | (read STATUS ; echo $STATUS > "+STATUS_FILE+")"
                    print("To execute: "+terminalCmd)
                    os.system(terminalCmd)
                    
                    readFromFile = ReadFromFile(STATUS_FILE)
                    for line in readFromFile.readLines():
                        STATUS = readFromFile.readLines()
                    
                    #STATUS = "COMPLETED"
                    print("Current STATUS: "+STATUS)
                    
                    # Only used for testing with Mirai
                    # TODO: Not sure how these should work.
                    #if (STATUS != "STARTED"):
                        #duration=$SECONDS
                        #echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
                        #if [ $MIRAI_STARTED -eq 0 ]
                        #if [ $SECONDS -gt 180 ]
                        #MIRAI_STARTED=1
                        #pass
                        
                    # cleanup
                    commonMethods.removeFileRelativePath(self.rootDirectory+"/"+STATUS_FILE)
                    # TODO: Uncomment
                    time.sleep(120)
                
                # Stop the resource data collection and store the data
                #echo "Data collection: "
                #curl http://$SUT_IP:$STAT_COLLECTOR_PORT/stop
                #echo ""
                
                # Execute commands after a test.
                for postExec in pptamConfigurationData.getPostExecExternalCommands():
                    print("")
                    print("------------------------------------")
                    print("    --- Execute external command ---")
                    os.system(postExec)
                    print("------------------------------------")
                    print("")
                
                print("Undeploying the system under test")
                # undeploy the system under test
                
                #terminalCmd = "cd "+self.rootDirectory+"/to_execute/"+testID 
                #os.system(terminalCmd)
                #cd ./to_execute/$TEST_ID/
                
                # undeploy the system under test       
                terminalCmd = "docker stack rm "+testFolder+"/"+testID+"/"+testID
                print("To execute: "+terminalCmd)
                os.system(terminalCmd)
                
                # be sure everything is clean
                terminalCmd = "docker stack rm $(docker stack ls --format \"{{.Name}}\") || true" 
                print("To execute: "+terminalCmd)
                os.system(terminalCmd)
                terminalCmd = "docker rm -f -v $(docker ps -a -q) || true" 
                os.system(terminalCmd)
                
                # saving test results
                print("Saving test results")
                os.mkdir(executedTests+"/"+testID)
                os.mkdir(executedTests+"/"+testID+"/faban")
                
                terminalCmd = "java -jar "+testExecutorDestination+"/faban/benchflow-faban-client/target/benchflow-faban-client.jar "+FABAN_MASTER+" info "+RUN_ID+" > executed/"+testID+"/faban/runInfo.txt" 
                print("To execute: "+terminalCmd)
                os.system(terminalCmd)
                
                fileOriginAbsPath = testExecutorDestination+"/faban/output/"+RUN_ID+"/summary.xml"
                folderTargetAbsPath = testExecutorDestination+"/executed/"+testID+"/faban/"
                commonMethods.copyFile(fileOriginAbsPath, folderTargetAbsPath)
                
                fileOriginAbsPath = testExecutorDestination+"/faban/output/"+RUN_ID+"/summary.xml"
                folderTargetAbsPath = testExecutorDestination+"/executed/"+testID+"/faban/"
                commonMethods.copyFileRel(fileOriginAbsPath, folderTargetAbsPath)
                
                fileOriginAbsPath = testExecutorDestination+"/faban/output/"+RUN_ID+"/log.xml"
                folderTargetAbsPath = testExecutorDestination+"/executed/"+testID+"/faban/"
                commonMethods.copyFileRel(fileOriginAbsPath, folderTargetAbsPath)
                #mkdir -p ./executed/$TEST_ID/stats
                # curl http://$SUT_IP:$STAT_COLLECTOR_PORT/data > executed/$TEST_ID/stats/cpu.txt
                #cp ./services/stats/cpu.txt ./executed/$TEST_ID/stats/cpu.txt
                folderOriginAbsPath = testExecutorDestination+"/to_execute/"+testID+"/"
                folderTargetAbsPath = testExecutorDestination+"/executed/"+testID+"/definition"
                commonMethods.moveFromFolder2Folder(fileOriginAbsPath, folderTargetAbsPath)