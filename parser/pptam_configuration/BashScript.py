import os
import subprocess
import random
import string
import json 

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
	def generateTests(self):
		systemConfigurationData = self.parseConfiguration.getSystemConfigurationData()

		# Get a random test id.
		# TODO: It can happen that two tests have the same id. Demand the test ID from the server?
		testID = self.randomString(32)

		print("Generate a test with ID="+testID)

		# Configure the template for this test in the tmp folder
  		#rm -rf ./drivers/tmp/*
  		#cp -aR ./templates/faban/driver/ecsa/* ./drivers/tmp/

		pptamConfigurationData = systemConfigurationData.getPPTAMConfigurationData()
		fabanConfigurationData = systemConfigurationData.getFabanConfigurationData()
		
  		# Configure the Faban driver
		self.replaceValueInFile("${FABAN_IP}", pptamConfigurationData.getFabanIP(), "build.properties")
		# Configure the Test ID
		self.replaceValueInFile("${TEST_NAME}", testID, "build.properties")
  		#FABAN_IP=$(getProperty "faban.ip")
  		#JAVA_HOME_FABAN=$(getProperty "java.home")
  		#sed -i.bak 's/${FABAN_IP}/'$FABAN_IP'/' ./drivers/tmp/build.properties
  		#sed -i.bak 's/${TEST_NAME}/'$TEST_ID'/' ./drivers/tmp/build.properties
  		#sed -i.bak 's/${JAVA_HOME_FABAN}/'$JAVA_HOME_FABAN'/' ./drivers/tmp/build.xml
  		#rm ./drivers/tmp/build.properties.bak
  		#rm ./drivers/tmp/build.xml.bak
#bench.shortname=${TEST_NAME}
#faban.home=../../faban
#faban.url=http://${FABAN_IP}:9980/
#deploy.user=admin
#deploy.password=adminadmin
#deploy.clearconfig=true
#compiler.source.version=1.7

#bench.shortname=oPCi9uI5YoQUIhX35yFF9rKSs0C7uI8n
#faban.home=../../faban
#faban.url=http://192.168.2.1:9980/
#deploy.user=admin
#deploy.password=adminadmin
#deploy.clearconfig=true
#compiler.source.version=1.7
	def replaceValueInFile(self, paramPlaceHolder, paramValue, pathToBuildProperties):
		readFromFile = ReadFromFile(pathToBuildProperties)

		print("Try to replace " + paramPlaceHolder + " with " + paramValue + ".")

		newFileDictionary = []

		# Rewrite the file
		for line in readFromFile.readLines():
			if (paramPlaceHolder in line):
				line = line.replace(paramPlaceHolder,paramValue)
				print("	Replace " + paramPlaceHolder + " with " + paramValue + ".")
				print("	Result: " + line + ".")
			#else:
				#print("Line "+line+" does not contain "+paramPlaceHolder+".")

			newFileDictionary.append(line)

		pathToBuildPropertiesTmp = "build.properties.tmp"
		writeToFile = WriteToFile(pathToBuildPropertiesTmp)
		writeToFile.overwriteTheExistingFile()

		for line in newFileDictionary:
			writeToFile.writeLine(line)

		for line in readFromFile.readLines():
			print(line)

		readFromFileTmp = ReadFromFile(pathToBuildPropertiesTmp)
		for line in readFromFile.readLines():
			print(line)
					
	def randomString(self, stringLength):
    	# Generate a random string of fixed length.
		letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
		return ''.join(random.choice(letters) for i in range(stringLength))

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