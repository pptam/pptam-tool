import os
import shutil
import subprocess
import json 
import time
import os.path
from os import path

from shutil import copyfile
from distutils.dir_util import copy_tree

# Import classes.
from configurationParser.pptam_configuration.ParseConfiguration import ParseConfiguration
from configurationParser.ReadFromFile import ReadFromFile
from configurationParser.WriteToFile import WriteToFile
from configurationParser.CommonMethods import CommonMethods

class PPTAMConfiguration():
	parseConfiguration = None
	# If the input is configuration.txt, parse it, get dictionary out of it, and create a json fine. Proceed with that json file.
	# If input is a json file, read it into a dictinary and use it to populate system configuration data in ParseConfiguration.
	def readConfiguration(self, configurationFilePath):
		configurationFilePath_JSON = configurationFilePath

		self.parseConfiguration = ParseConfiguration()

		# If the input is configuration.txt, parse it and create a json fine..
		if(configurationFilePath.endswith('txt')):
			print("readConfiguration::Convert text file to a JSON.")
			#dictionaryConf = parseConfiguration.getJSON_Dictionary() 
			self.parseConfiguration.parseConfigFile(configurationFilePath) 
			# Create a path to a text file, but .json extension.
			base = os.path.splitext(configurationFilePath)[0]
			configurationFilePath_JSON = base + '.json'
			# Create JSON file and write a dictionary in it.
			json_file = open(configurationFilePath_JSON, "w", encoding="utf-8")
			print("readConfiguration:JSON dictionary:")
			#print(self.parseConfiguration.getJSON_Dictionary())
			json.dump(self.parseConfiguration.getJSON_Dictionary(), json_file, ensure_ascii=False)
			json_file.close()

		#print("configurationFilePath_JSON = "+configurationFilePath_JSON)
		self.parseConfiguration.parseJSONConfigFile(configurationFilePath_JSON)

		print("configurationFilePath="+configurationFilePath)
		print("configurationFilePath_JSON="+configurationFilePath_JSON)
		print("Parsing system configuration --- COMPLETE.")

	# Copy necessary files to a test folder.
	# Change place holder values in these files.	
	def generateTests(self, testExecutorOrigin, fabanDriverDestination, driversDestination):
		
		commonMethods = CommonMethods()

		fabanTemplatesOrigin = testExecutorOrigin+"/templates"
		fabanDriverEcsaOrigin = fabanDriverDestination+"/driver/ecsa"

		systemConfigurationData = self.parseConfiguration.getSystemConfigurationData()

		# Get a random test id.
		# TODO: It can happen that two tests have the same id. Demand the test ID from the server?
		testID = commonMethods.randomString(32)

		print("Generate a test with ID="+testID)

		# Configure the template for this test in the tmp folder
		# - Check if drivers/tmp exists. If not, create it.
		#pathTmp = commonMethods.getCurrentPath()
		#pathTmp = ""
		#print("Current path = "+pathTmp)
		driversDestinationTmp = driversDestination+"/tmp"
		#print("fabanDriverEcsaDestinationTmp = "+fabanDriverEcsaDestinationTmp)
		# For some reason, the code below has an issue on Linux.
		# It removes the starting slash "/" sign.
		#try:
			# For nested paths, create folder per folder.
		#	for folderName in driversDestinationTmp.split("/"):
				# Avoid empty strings
		#		if not folderName:
		#			continue
				# The first input
		#		if pathTmp=="":
		#			pathTmp = folderName
		#		else:
		#			pathTmp = pathTmp+"/"+folderName
				# Avoid creating folders if they already exist.
		#		if os.path.isdir(pathTmp):
		#			continue
		#		os.mkdir(pathTmp)
		#except OSError:
		#	print ("Creation of the directory %s failed" % pathTmp)
		#else:
		#	print ("Successfully created the directory %s " % pathTmp)
		if path.isdir(driversDestination) == False:
			commonMethods.createFolderRelPath(driversDestination)
		if path.isdir(driversDestinationTmp) == False:
			commonMethods.createFolderRelPath(driversDestinationTmp)
		
		# Delete all files in the temp folder
		print("Delete all files from path = "+driversDestinationTmp)
		commonMethods.deleteFilesFromFolder(driversDestinationTmp)

		# Copy FABAN files
		commonMethods.copyFromFolder2Folder(fabanDriverEcsaOrigin, driversDestinationTmp)
		
		pptamConfigurationData = systemConfigurationData.getPPTAMConfigurationData()
		fabanConfigurationData = systemConfigurationData.getFabanConfigurationData()
		dockerConfigurationData = systemConfigurationData.getDockerConfigurationData()
		
  		# Configure the Faban driver - build.properties
		commonMethods.replaceValueInFile("${FABAN_IP}", pptamConfigurationData.getFabanIP(), driversDestinationTmp+"/build.properties")
		# Configure the Test ID - build.properties
		commonMethods.replaceValueInFile("${TEST_NAME}", testID, driversDestinationTmp+"/build.properties")
		# Configure JAVA_HOME_FABAN - run.xml
		commonMethods.replaceValueInFile("${JAVA_HOME_FABAN}", pptamConfigurationData.getJavaHomeFaban(), driversDestinationTmp+"/build.xml")

		# Remove bak files
		commonMethods.removeFileRelativePath(driversDestinationTmp+"/build.properties.bak")
		commonMethods.removeFileRelativePath(driversDestinationTmp+"/build.xml.bak")
		# rm ./drivers/tmp/build.properties.bak
		# rm ./drivers/tmp/build.xml.bak
		
		# Deploy
		# Configure TEST_ID - run.xml
		#./drivers/tmp/deploy/run.xml
		pathTmpDeployRun = driversDestinationTmp+"/deploy/run.xml"
		commonMethods.replaceValueInFile("${TEST_NAME}", testID, pathTmpDeployRun)
		# Configure FABAN_IP - run.xml
		commonMethods.replaceValueInFile("${FABAN_IP}", pptamConfigurationData.getFabanIP(), pathTmpDeployRun)
		# Configure NUM_USERS - run.xml
		commonMethods.replaceValueInFile("${NUM_USERS}", fabanConfigurationData.getNumberOfUsers(), pathTmpDeployRun)
		# Configure FABAN_OUTPUT_DIR - run.xml
		commonMethods.replaceValueInFile("${FABAN_OUTPUT_DIR}", pptamConfigurationData.getfabanOutputDir(), pathTmpDeployRun)
		# Configure SUT_IP - run.xml
		commonMethods.replaceValueInFile("${SUT_IP}", pptamConfigurationData.getSutIP(), pathTmpDeployRun)
		# Configure SUT_PORT - run.xml
		commonMethods.replaceValueInFile("${SUT_PORT}", pptamConfigurationData.getSutPort(), pathTmpDeployRun)
		# Config (just replace with the one generated for deploy)
		pathTmpConfigRun = driversDestinationTmp+"/config/"
		commonMethods.copyFileRel(pathTmpDeployRun, pathTmpConfigRun)
  		#yes | cp -rf ./drivers/tmp/deploy/run.xml ./drivers/tmp/config/run.xml

		# Remove bak file.
		commonMethods.removeFileRelativePath(driversDestinationTmp+"/deploy/run.xml.bak")
	    #rm ./drivers/tmp/deploy/run.xml.bak
		
		# Configure testID - WebDriver.java
		commonMethods.replaceValueInFile("${TEST_NAME}", testID, driversDestinationTmp+"/src/ecsa/driver/WebDriver.java")
	
		# Remove bak file
		commonMethods.removeFileRelativePath(driversDestinationTmp+"/src/ecsa/driver/WebDriver.java.bak")
		# rm ./drivers/tmp/src/ecsa/driver/WebDriver.java.bak
		
		# Configure the deployment descriptor
		#print("fabanTemplatesOrigin = "+fabanTemplatesOrigin)
		dockerFileOrigin = fabanTemplatesOrigin+"/deployment_descriptor/template/docker-compose.yml"
		dockerFolderTarget = driversDestinationTmp+"/deploy"
		commonMethods.copyFileRel(dockerFileOrigin, dockerFolderTarget)
		
  		#cp -aR ./templates/deployment_descriptor/template/docker-compose.yml ./drivers/tmp/deploy
		# Configure SUT_HOSTNAME - docker-compose.yml
		commonMethods.replaceValueInFile("${SUT_HOSTNAME}", pptamConfigurationData.getSutHostname(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_REPLICAS - docker-compose.yml
		commonMethods.replaceValueInFile("${CARTS_REPLICAS}", dockerConfigurationData.getNumOfReplicas(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_CPUS_LIMITS - docker-compose.yml
		commonMethods.replaceValueInFile("${CARTS_CPUS_LIMITS}", dockerConfigurationData.getCpuLimit(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_CPUS_RESERVATIONS - docker-compose.yml
		commonMethods.replaceValueInFile("${CARTS_CPUS_RESERVATIONS}", dockerConfigurationData.getCpuReservation(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_RAM_LIMITS - docker-compose.yml
		commonMethods.replaceValueInFile("${CARTS_RAM_LIMITS}", dockerConfigurationData.getRamLimit(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_RAM_RESERVATIONS - docker-compose.yml
		commonMethods.replaceValueInFile("${CARTS_RAM_RESERVATIONS}", dockerConfigurationData.getRamReservation(), dockerFolderTarget+"/docker-compose.yml")
		
		commonMethods.removeFileRelativePath(dockerFolderTarget+"/docker-compose.yml.bak")
		#rm ./drivers/tmp/deploy/docker-compose.yml.bak
		
		# create a folder for the new test and copy the tmp data
		commonMethods.createFolderRelPath(driversDestination+"/"+testID)
		# Move all files from tmp to a created folder that coresponds to a test.
		# - First copy, then delete.
		#self.moveFromFolder2Folder(fabanDriverEcsaDestinationTmp, fabanDriverDestination+"/"+testID)
		commonMethods.copyFromFolder2Folder(driversDestinationTmp, driversDestination+"/"+testID)
		commonMethods.deleteFilesFromFolder(driversDestinationTmp)
			
  		#mkdir -p ./drivers/$TEST_ID
		#cp -aR ./drivers/tmp/* ./drivers/$TEST_ID
		#rm -rf ./drivers/tmp/*

		# Compile and package for deploy the faban driver
		print("Compiling the Faban driver")
		#os.system("cwd=$(pwd)")
		#terminalCmd = "cd ./drivers/"+testID
		#terminalCmd = "cd "+fabanDriverDestination+"/"+testID
		#os.system(terminalCmd)
		#ant -Dbasedir=`pwd` -f path/to/build.xml
		#os.system("ant "+fabanDriverDestination+"/"+testID+" deploy.jar")
		terminalCmd="ant -f "+driversDestination+"/"+testID+"/build.xml deploy.jar"
		print("To execute: "+terminalCmd)
		os.system(terminalCmd)
		#os.system("cd \"$cwd\"")
		#cwd=$(pwd)
		#cd ./drivers/$TEST_ID
		#ant deploy.jar
		#cd "$cwd"
		
		# create a folder for the test
		newDir = testExecutorOrigin+"/to_execute"
		if path.isdir(newDir):
			pass
		else:
			commonMethods.createFolderRelPath(newDir)
			
		newDir = testExecutorOrigin+"/to_execute/"+testID
		if path.isdir(newDir):
			pass
		else:
			commonMethods.createFolderRelPath(newDir)

		# mkdir -p ./to_execute/$TEST_ID
		# copy the driver jarm run.xml and deployment descriptor
		commonMethods.copyFileRel(driversDestination+"/"+testID+"/build/"+testID+".jar", testExecutorOrigin+"/to_execute/"+testID)
		# cp ./drivers/$TEST_ID/build/$TEST_ID.jar ./to_execute/$TEST_ID
		commonMethods.copyFileRel(driversDestination+"/"+testID+"/config/run.xml", testExecutorOrigin+"/to_execute/"+testID)
		# cp ./drivers/$TEST_ID/config/run.xml ./to_execute/$TEST_ID
		commonMethods.copyFileRel(driversDestination+"/"+testID+"/deploy/docker-compose.yml", testExecutorOrigin+"/to_execute/"+testID)
		# cp ./drivers/$TEST_ID/deploy/docker-compose.yml ./to_execute/$TEST_ID
	
	# To delete, not used anymore.
	def executeTests(self, rootDirectory):
		systemConfigurationData = self.parseConfiguration.getSystemConfigurationData()
		pptamConfigurationData = systemConfigurationData.getPPTAMConfigurationData()
		fabanConfigurationData = systemConfigurationData.getFabanConfigurationData()
		dockerConfigurationData = systemConfigurationData.getDockerConfigurationData()

		FABAN_IP = pptamConfigurationData.getFabanIP()
		#FABAN_IP=$(getProperty "faban.ip")
		FABAN_MASTER = "http://"+pptamConfigurationData.getFabanIP()+":"+pptamConfigurationData.getSutPort()+"/"
		#FABAN_MASTER="http://$FABAN_IP:9980/";
		# TODO: should we configure FABAN_CLIENT externally?
		FABAN_CLIENT="./faban/benchflow-faban-client/target/benchflow-faban-client.jar"
		SUT_IP=pptamConfigurationData.getSutIP()
		#SUT_IP=$(getProperty "sut.ip")
		#STAT_COLLECTOR_PORT=$(getProperty "stat.collector.port")
		
		# Get all test folders - test IDs.
		testFolder = rootDirectory+"/test_executor/to_execute/"
		print("Execute tests from "+testFolder)
		for f in os.scandir(testFolder):
			# Execute commands before a test.
			for preExec in pptamConfigurationData.getPreExecExternalCommands():
				os.system(preExec)
				
			if f.is_dir():
				testID = f
				print("Starting test: "+testID)
				print("Deploying the system under test")
				
				terminalCmd = "cd ./to_execute/"+testID 
				os.system(terminalCmd)
				terminalCmd = "docker stack deploy --compose-file=docker-compose.yml "+testID 
				os.system(terminalCmd)
				
				print("Waiting for the system to be ready")
				time.sleep(120)
				#terminalCmd = "sleep 120"
				#os.system(terminalCmd)
				
				terminalCmd = "export "+testID 
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
				
				# Cleanup
				removeFileRelativePath(RUN_ID_FILE)
				
				print("Run ID: "+RUN_ID)
				
				
				# Wait for the test to be done.
				STATUS=""
				
				while ( (STATUS != "COMPLETED") and (STATUS != "COMPLETED")):
					STATUS_FILE = "STATUS.txt"
					
					terminalCmd = "java -jar ./faban/benchflow-faban-client/target/benchflow-faban-client.jar"++" status $RUN_ID | (read STATUS ; echo $STATUS > "+STATUS_FILE+")"
					
					readFromFile = ReadFromFile(STATUS_FILE)
					for line in readFromFile.readLines():
						STATUS = readFromFile.readLines()
					
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
					os.remove(STATUS_FILE)
					
					time.sleep(120)
				
				# Stop the resource data collection and store the data
				#echo "Data collection: "
				#curl http://$SUT_IP:$STAT_COLLECTOR_PORT/stop
				#echo ""
				
				# Execute commands after a test.
				for postExec in pptamConfigurationData.getPostExecExternalCommands():
					os.system(postExec)
				
				print("Undeploying the system under test")
				# undeploy the system under test
				
				terminalCmd = "cd "+rootDirectory+"/"+testID 
				os.system(terminalCmd)
				#cd ./to_execute/$TEST_ID/
				
				terminalCmd = "docker stack rm"+testID 
				os.system(terminalCmd)
				
				# be sure everything is clean
				terminalCmd = "docker stack rm $(docker stack ls --format \"{{.Name}}\") || true" 
				os.system(terminalCmd)
				terminalCmd = "docker rm -f -v $(docker ps -a -q) || true" 
				os.system(terminalCmd)
				
				# saving test results
				print("Saving test results")
				
				os.mkdir(rootDirectory+"/test_executor/executed/"+testID)
				os.mkdir(rootDirectory+"/test_executor/executed/"+testID+"/faban")
				
				terminalCmd = "java -jar ./faban/benchflow-faban-client/target/benchflow-faban-client.jar "+FABAN_MASTER+" info "+RUN_ID+" > executed/"+testID+"/faban/runInfo.txt" 
				os.system(terminalCmd)
				
				fileOriginRelPath = "./faban/output/"+RUN_ID+"/summary.xml"
				fileTargetRelPath = "./executed/"+testID+"/faban/"
				copyFileRel(fileOriginRelPath, fileTargetRelPath)
				
				fileOriginRelPath = "./faban/output/"+RUN_ID+"/summary.xml"
				fileTargetRelPath = "./executed/"+testID+"/faban/"
				copyFileRel(fileOriginRelPath, fileTargetRelPath)
				
				fileOriginRelPath = "./faban/output/"+RUN_ID+"/log.xml"
				fileTargetRelPath = "./executed/"+testID+"/faban/"
				copyFileRel(fileOriginRelPath, fileTargetRelPath)
				#mkdir -p ./executed/$TEST_ID/stats
				# curl http://$SUT_IP:$STAT_COLLECTOR_PORT/data > executed/$TEST_ID/stats/cpu.txt
				#cp ./services/stats/cpu.txt ./executed/$TEST_ID/stats/cpu.txt
				folderOriginRelPath = "./to_execute/"+testID+"/"
				folderTargetRelPath = "./executed/"+testID+"/definition"
				moveFromFolder2Folder(folderOriginRelPath, folderTargetRelPath)
	
	def getParseConfiguration(self):
		return self.parseConfiguration
				

def generate_test(NUM_USERS, CARTS_REPLICAS, CARTS_CPUS_LIMITS, CARTS_CPUS_RESERVATIONS, CARTS_RAM_LIMITS, CARTS_RAM_RESERVATIONS):
	# head -n 1 - shows the first line of a text file.
	# fold -w 32 - fold command in Linux wraps each line in an input file to fit a specified width and prints it to the standard output
	# tr -dc 'a-zA-Z0-9'- tr command in UNIX is a command line utility for translating or deleting characters.
	#out = subprocess.Popen(['cat ', '/dev/urandom', '|', 'env', 'LC_CTYPE=C', 'tr', '-dc', '\'a-zA-Z0-9\'', '|', 'fold', '-w', '32', '|', 'head', '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	#stdout,stderr = out.communicate()
	#print(stdout)
	#process = subprocess.run(['cat /dev/urandom | env LC_CTYPE=C tr -dc \'a-zA-Z0-9\' | fold -w 32 | head -n 1'], stdout=subprocess.PIPE, universal_newlines=True)
	# Generate a random number.
	myCmd = os.popen('cat /dev/urandom | env LC_CTYPE=C tr -dc \'a-zA-Z0-9\' | fold -w 32 | head -n 1').read()
	print(myCmd+", length "+str(len(myCmd))+".")
	#myCmd = os.popen('ls -la').read()
	#print(myCmd)