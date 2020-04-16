import os
import shutil
from shutil import copyfile
import subprocess
import random
import string
import json 
from distutils.dir_util import copy_tree

from ParseConfiguration import ParseConfiguration
from ReadFromFile import ReadFromFile
from WriteToFile import WriteToFile

class BashScript():
	parseConfiguration = None

	# If the input is configuration.txt, parse it, get dictionary out of it, and create a json fine. Proceed with that json file.
	# If input is a json file, read it into a dictinary and use it to populate system configuration data in ParseConfiguration.
	def readConfiguration(self, configurationFilePath):
		configurationFilePath_JSON = configurationFilePath

		self.parseConfiguration = ParseConfiguration()

		# If the input is configuration.txt, parse it and create a json fine..
		if(configurationFilePath.endswith('txt')):
			#dictionaryConf = parseConfiguration.getJSON_Dictionary() 
			self.parseConfiguration.parseConfigFile(configurationFilePath) 
			# Create a path to a text file, but .json extension.
			base = os.path.splitext(configurationFilePath)[0]
			configurationFilePath_JSON = base + '.json'
			# Create JSON file and write a dictionary in it.
			json_file = open(configurationFilePath_JSON, "w", encoding="utf-8")
			print("readConfiguration:JSON dictionary:")
			print(self.parseConfiguration.getJSON_Dictionary())
			print(self.parseConfiguration.getJSON_Dictionary())
			json.dump(self.parseConfiguration.getJSON_Dictionary(), json_file, ensure_ascii=False)
			json_file.close()

		print(configurationFilePath_JSON)
		self.parseConfiguration.parseJSONConfigFile(configurationFilePath_JSON)

		print("configurationFilePath="+configurationFilePath)
		print("configurationFilePath_JSON="+configurationFilePath_JSON)
		print("Parsing system configuration --- COMPLETE.")

	# Copy necessary files to a test folder.
	# Change place holder values in these files.	
	def generateTests(self, testExecutorOrigin, fabanDriverDestination):

		fabanTemplatesOrigin = testExecutorOrigin+"/templates"
		fabanDriverEcsaOrigin = fabanTemplatesOrigin+"/faban/driver/ecsa"

		systemConfigurationData = self.parseConfiguration.getSystemConfigurationData()

		# Get a random test id.
		# TODO: It can happen that two tests have the same id. Demand the test ID from the server?
		testID = self.randomString(32)

		print("Generate a test with ID="+testID)

		# Configure the template for this test in the tmp folder
		# - Check if drivers/tmp exists. If not, create it.
		pathTmp = self.getCurrentPath()
		fabanDriverEcsaDestinationTmp = fabanDriverDestination+"/tmp"
		try:
			# For nested paths, create folder per folder.
			for folderName in fabanDriverEcsaDestinationTmp.split("/"):
				if not folderName:
					continue
				pathTmp = pathTmp+"/"+folderName
				# Avoid creating folders if they already exist.
				if os.path.isdir(pathTmp):
					continue
				os.mkdir(pathTmp)
		except OSError:
			print ("Creation of the directory %s failed" % pathTmp)
		else:
			print ("Successfully created the directory %s " % pathTmp)
		
		# Delete all files in the temp folder
		self.deleteFilesFromFolder(pathTmp)

		# Copy FABAN files
		self.copyFromFolder2Folder(fabanDriverEcsaOrigin, fabanDriverEcsaDestinationTmp)
		
		pptamConfigurationData = systemConfigurationData.getPPTAMConfigurationData()
		fabanConfigurationData = systemConfigurationData.getFabanConfigurationData()
		dockerConfigurationData = systemConfigurationData.getDockerConfigurationData()
		
  		# Configure the Faban driver - build.properties
		self.replaceValueInFileRelPath("${FABAN_IP}", pptamConfigurationData.getFabanIP(), pathTmp+"/build.properties")
		# Configure the Test ID - build.properties
		self.replaceValueInFileRelPath("${TEST_NAME}", testID, pathTmp+"/build.properties")
		# Configure JAVA_HOME_FABAN - run.xml
		self.replaceValueInFileRelPath("${JAVA_HOME_FABAN}", pptamConfigurationData.getJavaHomeFaban(), pathTmp+"/build.xml")

		# Remove bak files
		self.removeFileRelativePath(pathTmp+"/build.properties.bak")
		self.removeFileRelativePath(pathTmp+"/build.xml.bak")
		# rm ./drivers/tmp/build.properties.bak
		# rm ./drivers/tmp/build.xml.bak
		
		# Deploy
		# Configure TEST_ID - run.xml
		#./drivers/tmp/deploy/run.xml
		pathTmpDeployRun = pathTmp+"/deploy/run.xml"
		self.replaceValueInFileRelPath("${TEST_NAME}", testID, pathTmpDeployRun)
		# Configure FABAN_IP - run.xml
		self.replaceValueInFileRelPath("${FABAN_IP}", pptamConfigurationData.getFabanIP(), pathTmpDeployRun)
		# Configure NUM_USERS - run.xml
		self.replaceValueInFileRelPath("${NUM_USERS}", fabanConfigurationData.getNumberOfUsers(), pathTmpDeployRun)
		# Configure FABAN_OUTPUT_DIR - run.xml
		self.replaceValueInFileRelPath("${FABAN_OUTPUT_DIR}", pptamConfigurationData.getfabanOutputDir(), pathTmpDeployRun)
		# Configure SUT_IP - run.xml
		self.replaceValueInFileRelPath("${SUT_IP}", pptamConfigurationData.getSutIP(), pathTmpDeployRun)
		# Configure SUT_PORT - run.xml
		self.replaceValueInFileRelPath("${SUT_PORT}", pptamConfigurationData.getSutPort(), pathTmpDeployRun)
		# Config (just replace with the one generated for deploy)
		pathTmpConfigRun = pathTmp+"/config/"
		self.copyFileRel(pathTmpDeployRun, pathTmpConfigRun)
  		#yes | cp -rf ./drivers/tmp/deploy/run.xml ./drivers/tmp/config/run.xml

		# Remove bak file.
		self.removeFileRelativePath(pathTmp+"/deploy/run.xml.bak")
	    #rm ./drivers/tmp/deploy/run.xml.bak
		
		# Configure testID - WebDriver.java
		self.replaceValueInFileRelPath("${TEST_NAME}", testID, pathTmp+"/src/ecsa/driver/WebDriver.java")
	
		# Remove bak file
		self.removeFileRelativePath(pathTmp+"/src/ecsa/driver/WebDriver.java.bak")
		# rm ./drivers/tmp/src/ecsa/driver/WebDriver.java.bak
		
		# Configure the deployment descriptor
		#print("fabanTemplatesOrigin = "+fabanTemplatesOrigin)
		dockerFileOrigin = fabanTemplatesOrigin+"/deployment_descriptor/template/docker-compose.yml"
		dockerFolderTarget = pathTmp+"/deploy"
		self.copyFileRel(dockerFileOrigin, dockerFolderTarget)
		
  		#cp -aR ./templates/deployment_descriptor/template/docker-compose.yml ./drivers/tmp/deploy
		# Configure SUT_HOSTNAME - docker-compose.yml
		self.replaceValueInFileRelPath("${SUT_HOSTNAME}", pptamConfigurationData.getSutHostname(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_REPLICAS - docker-compose.yml
		self.replaceValueInFileRelPath("${CARTS_REPLICAS}", dockerConfigurationData.getNumOfReplicas(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_CPUS_LIMITS - docker-compose.yml
		self.replaceValueInFileRelPath("${CARTS_CPUS_LIMITS}", dockerConfigurationData.getCpuLimit(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_CPUS_RESERVATIONS - docker-compose.yml
		self.replaceValueInFileRelPath("${CARTS_CPUS_RESERVATIONS}", dockerConfigurationData.getCpuReservation(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_RAM_LIMITS - docker-compose.yml
		self.replaceValueInFileRelPath("${CARTS_RAM_LIMITS}", dockerConfigurationData.getRamLimit(), dockerFolderTarget+"/docker-compose.yml")
		# Configure CARTS_RAM_RESERVATIONS - docker-compose.yml
		self.replaceValueInFileRelPath("${CARTS_RAM_RESERVATIONS}", dockerConfigurationData.getRamReservation(), dockerFolderTarget+"/docker-compose.yml")
		
		self.removeFileRelativePath(dockerFolderTarget+"/docker-compose.yml.bak")
		#rm ./drivers/tmp/deploy/docker-compose.yml.bak
		
		# create a folder for the new test and copy the tmp data
		self.createFolderRelPath(fabanDriverDestination+"/"+testID)
		# Move all files from tmp to a created folder that coresponds to a test.
		# - First copy, then delete.
		#self.moveFromFolder2Folder(fabanDriverEcsaDestinationTmp, fabanDriverDestination+"/"+testID)
		self.copyFromFolder2Folder(fabanDriverEcsaDestinationTmp, fabanDriverDestination+"/"+testID)
		self.deleteFilesFromFolder(fabanDriverEcsaDestinationTmp)
			
  		#mkdir -p ./drivers/$TEST_ID
		#cp -aR ./drivers/tmp/* ./drivers/$TEST_ID
		#rm -rf ./drivers/tmp/*

		# Compile and package for deploy the faban driver
		print("Compiling the Faban driver")
		#os.system("cwd=$(pwd)")
		terminalCmd = "cd ./drivers/"+testID
		os.system(terminalCmd)
		os.system("ant deploy.jar")
		#os.system("cd \"$cwd\"")
		#cwd=$(pwd)
		#cd ./drivers/$TEST_ID
		#ant deploy.jar
		#cd "$cwd"
		
		# create a folder for the test
		self.createFolderRelPath(testExecutorOrigin+"/to_execute")
		self.createFolderRelPath(testExecutorOrigin+"/to_execute/"+testID)
		# mkdir -p ./to_execute/$TEST_ID
		# copy the driver jarm run.xml and deployment descriptor
		self.copyFileRel(fabanDriverDestination+"/"+testID+"/build/"+testID+".jar", testExecutorOrigin+"/to_execute/"+testID)
		# cp ./drivers/$TEST_ID/build/$TEST_ID.jar ./to_execute/$TEST_ID
		self.copyFileRel(fabanDriverDestination+"/"+testID+"/config/run.xml", testExecutorOrigin+"/to_execute/"+testID)
		# cp ./drivers/$TEST_ID/config/run.xml ./to_execute/$TEST_ID
		self.copyFileRel(fabanDriverDestination+"/"+testID+"/deploy/docker-compose.yml", testExecutorOrigin+"/to_execute/"+testID)
		# cp ./drivers/$TEST_ID/deploy/docker-compose.yml ./to_execute/$TEST_ID
	
	def executeTests():
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
    	for f in os.scandir(folder):
    	 	if f.is_dir():
    	 		print("Starting test: $TEST_ID")
    	 		print("Deploying the system under test")
    	 		testID = f
    	 		terminalCmd = "cd ./to_execute/"+testID 
    	 		os.system(terminalCmd)
    	 		
    	 		terminalCmd = "docker stack deploy --compose-file=docker-compose.yml "+testID 
    	 		os.system(terminalCmd)
    	 		
    	 		print("Waiting for the system to be ready")
    	 		terminalCmd = "sleep 120"
    	 		os.system(terminalCmd)
    	 		
    	 		terminalCmd = "export "+testID 
    	 		os.system(terminalCmd)
    	 		
    	 		test_name=testID
    	 		driver="to_execute/"+testID+"/"+testID+".jar"
            	driver_conf="to_execute/"+testID+"/run.xml"
             	deployment_descriptor="to_execute/"+testID+"/docker-compose.yml"
             	
             	print("Deploying the load driver")
             	# Deploy and start the test
             	terminalCmd = "java -jar "+FABAN_CLIENT+" "+FABAN_MASTER+" deploy "+test_name+" "+driver+" "+driver_conf+" | (read RUN_ID ; echo $RUN_ID > RUN_ID.txt)"
             	os.system(terminalCmd)
    
    # Create folder with relative path.
	def createFolderRelPath(self, path):
		try:
			# Create target Directory
			os.mkdir(path)
			print("Directory " , path ,  " Created ")
		except FileExistsError:
			print("Directory " , path ,  " already exists")

	# Copy all files and folders from a folder to a folder.
	def copyFromFolder2Folder(self, folderOriginRelPath, folderTargetRelPath):
		currentPath = self.getCurrentPath()
		folderOriginAbsPath = os.path.join(currentPath, folderOriginRelPath)
		folderTargetAbsPath = os.path.join(currentPath, folderTargetRelPath)
		if not os.path.isdir(folderOriginAbsPath):
			print(folderOriginAbsPath+" -- no such path!")
			return
		if not os.path.isdir(folderTargetAbsPath):
			print(folderTargetAbsPath+" -- no such path!")
			return
		# Copy all from origin to destination.
		try:
			copy_tree(folderOriginAbsPath, folderTargetAbsPath)
		except:
			print("Copy failed.")
	
	# Move all files and folders from a folder to a folder.
	def moveFromFolder2Folder(self, folderOriginRelPath, folderTargetRelPath):
		currentPath = self.getCurrentPath()
		folderOriginAbsPath = os.path.join(currentPath, folderOriginRelPath)
		folderTargetAbsPath = os.path.join(currentPath, folderTargetRelPath)

		filesToMove = os.listdir(folderOriginRelPath)
		
		for f in filesToMove:
			shutil.move(folderOriginAbsPath+f, folderTargetRelPath)

	def removeFileRelativePath(self, pathRel):
		currentPath = self.getCurrentPath()
		pathAbs = os.path.join(currentPath, pathRel)
		if not os.path.isfile(pathAbs):
			#print("File " + pathAbs + " does not exist.")
			return
		else:
			try:
				os.remove("ChangedFile.csv")
			except:
				print("Cannot delete file " + pathAbs + " does not exist.")

	# Create temp file, instead of replacing the existing file.
	def replaceValueInFileWithTempFile(self, paramPlaceHolder, paramValue, pathToBuildProperties):
		readFromFile = None
		
		if (os.path.isfile(pathToBuildProperties+".tmp")):
			readFromFile = ReadFromFile(pathToBuildProperties+".tmp")
		elif (os.path.isfile(pathToBuildProperties)):
			readFromFile = ReadFromFile(pathToBuildProperties)
		else:
			print("replaceValueInFileWithTempFile:No file at "+pathToBuildProperties+".")
			return

		#print("Try to replace " + paramPlaceHolder + " with " + paramValue + ".")

		newFileDictionary = []

		# Rewrite the file
		# Attention: there could be several instances to replace. Replace them all.
		for line in readFromFile.readLines():
			if (paramPlaceHolder in line):
				line = line.replace(paramPlaceHolder,paramValue)
				#print("	Replace " + paramPlaceHolder + " with " + paramValue + ".")
				#print("	Result: " + line + ".")
			#else:
				#print("Line "+line+" does not contain "+paramPlaceHolder+".")

			newFileDictionary.append(line)

		pathToBuildPropertiesTmp = pathToBuildProperties+".tmp"
		writeToFile = WriteToFile(pathToBuildPropertiesTmp)
		writeToFile.overwriteTheExistingFile()

		for line in newFileDictionary:
			writeToFile.writeLine(line)

		for line in readFromFile.readLines():
			print(line)

		readFromFileTmp = ReadFromFile(pathToBuildPropertiesTmp)
		for line in readFromFile.readLines():
			print(line)

	# Read file, replace the value, overwrite the file.
	def replaceValueInFileRelPath(self, paramPlaceHolder, paramValue, pathToFileOrigin):
		readFromFile = None

		currentPath = self.getCurrentPath()
		pathToFileOriginAbs = os.path.join(currentPath, pathToFileOrigin)
		
		if (os.path.isfile(pathToFileOriginAbs)):
			readFromFile = ReadFromFile(pathToFileOriginAbs)
			# print("replaceValueInFileRelPath "+pathToFileOriginAbs+".")
		else:
			print("replaceValueInFileRelPath: No file at "+pathToFileOriginAbs+" !!!")
			return

		#print("Try to replace " + paramPlaceHolder + " with " + paramValue + ".")

		newFileDictionary = []

		# Rewrite the file
		# Attention: there could be several instances to replace. Replace them all.
		for line in readFromFile.readLines():
			if (paramPlaceHolder in line):
				line = line.replace(paramPlaceHolder,paramValue)
				#print("	Replace " + paramPlaceHolder + " with " + paramValue + ".")
				#print("	Result: " + line + ".")
			#else:
				#print("Line "+line+" does not contain "+paramPlaceHolder+".")

			newFileDictionary.append(line)

		writeToFile = WriteToFile(pathToFileOrigin)
		writeToFile.overwriteTheExistingFile()

		for line in newFileDictionary:
			writeToFile.writeLine(line)

		#for line in readFromFile.readLines():
			#print(line)

		#readFromFileTmp = ReadFromFile(pathToBuildPropertiesTmp)
		#for line in readFromFile.readLines():
			#print(line)


	def copyFileRel(self, fileOriginRelPath, fileTargetRelPath):
		currentPath = self.getCurrentPath()
		fileOriginAbsPath = os.path.join(currentPath, fileOriginRelPath)
		fileTargetAbsPath = os.path.join(currentPath, fileTargetRelPath)

		#print("Copy from "+fileOriginAbsPath+" -> " +fileTargetAbsPath)
		if not os.path.isfile(fileOriginAbsPath):
			print(fileOriginAbsPath+" -- no such file!")
			return
		if not os.path.isdir(fileTargetAbsPath):
			print(fileTargetAbsPath+" -- no such target dir!")
			return
		# Copy all from origin to destination.
		try:
			shutil.copy2(fileOriginAbsPath, fileTargetAbsPath)
		except:
			print("Copy failed.")

	def randomString(self, stringLength):
    	# Generate a random string of fixed length.
		letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
		return ''.join(random.choice(letters) for i in range(stringLength))
	
	# Get current path.
	def getCurrentPath(self):
		return os.path.dirname(os.path.abspath(__file__))

	# Delete all files from folder.
	def deleteFilesFromFolder(self, folderPath):
		for filename in os.listdir(folderPath):
			file_path = os.path.join(folderPath, filename)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))
				return
		print("Folder "+folderPath+" cleansed!")

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




NUM_USERS=50
CARTS_REPLICAS=1
CARTS_CPUS_LIMITS=0.25
CARTS_CPUS_RESERVATIONS=0.25
CARTS_RAM_LIMITS="500M"
CARTS_RAM_RESERVATIONS="500M"

#generate_test(NUM_USERS, CARTS_REPLICAS, CARTS_CPUS_LIMITS, CARTS_CPUS_RESERVATIONS, CARTS_RAM_LIMITS, CARTS_RAM_RESERVATIONS)

#TEST_ID = randomString(32)
#print(TEST_ID+", length "+str(len(TEST_ID))+".")