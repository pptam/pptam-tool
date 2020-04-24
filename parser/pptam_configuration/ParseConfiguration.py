# Read from file (file that was passed as a constructor).
# Create a Python dictionary, ready for writting to a JSON file.

import json 

from FileHandler import FileHandler
from ReadFromFile import ReadFromFile
from system_configuration.SystemConfigurationData import SystemConfigurationData


class ParseConfiguration():
    # Parsed data into a class.
    systemConfigurationData=None
    # JSON dictionary
    configurationJSON=None

    # Reads a config file with .txt extension and extracts JSON dictionary.
    # Sets JSON dictionary to a member of this class - configurationJSON.
    def parseConfigFile(self, fileName):
        FileHandler(fileName)
        readFromFile = ReadFromFile(fileName)
        print("ParseConfiguration::parseConfigFile::opened = "+fileName);
        # Dictionary.
        self.configurationJSON={}
        self.configurationJSON["PPTAM_Configuration"]={}
        self.configurationJSON["Faban_Configuration"]={}
        self.configurationJSON["Docker_Configuration"]={}
        FABAN_IP = JAVA_HOME_FABAN = FABAN_OUTPUT_DIR = SUT_IP = SUT_PORT = SUT_HOSTNAME = None
        CARTS_CPUS_LIMITS = CARTS_CPUS_RESERVATIONS = CARTS_RAM_LIMITS = CARTS_RAM_RESERVATIONS = CARTS_REPLICAS = None
        NUM_USERS = None
        print(readFromFile.readLines())
        print("ParseConfiguration::parseConfigFile::configurtion::to JSON file");
        for line in readFromFile.readLines():
            print("Loop")
            # Avoid comments and empty spaces.
            if line.startswith("#") or len(line)==0:
                continue
            #print(line)
            # PPTAM configuration
            if line.startswith("FABAN_IP"):
                FABAN_IP = line.split("=")
                self.configurationJSON["PPTAM_Configuration"]["FABAN_IP"]=FABAN_IP[1]
                print("Add FABAN IP="+FABAN_IP[1]+" to the configuration.")
            elif line.startswith("JAVA_HOME_FABAN"):
                JAVA_HOME_FABAN = line.split("=")
                self.configurationJSON["PPTAM_Configuration"]["JAVA_HOME_FABAN"]=JAVA_HOME_FABAN[1]
            elif line.startswith("FABAN_OUTPUT_DIR"):
                FABAN_OUTPUT_DIR = line.split("=")
                self.configurationJSON["PPTAM_Configuration"]["FABAN_OUTPUT_DIR"]=FABAN_OUTPUT_DIR[1]
            elif line.startswith("SUT_IP"):
                SUT_IP = line.split("=")
                self.configurationJSON["PPTAM_Configuration"]["SUT_IP"]=SUT_IP[1]
            elif line.startswith("SUT_PORT"):
                SUT_PORT = line.split("=")
                self.configurationJSON["PPTAM_Configuration"]["SUT_PORT"]=SUT_PORT[1]
            # Docker configuration
            elif line.startswith("SUT_HOSTNAME"):
                SUT_HOSTNAME = line.split("=")
                self.configurationJSON["PPTAM_Configuration"]["SUT_HOSTNAME"]=SUT_HOSTNAME[1]
            elif line.startswith("CARTS_CPUS_LIMITS"):
                CARTS_CPUS_LIMITS = line.split("=")
                self.configurationJSON["Docker_Configuration"]["CARTS_CPUS_LIMITS"]=CARTS_CPUS_LIMITS[1]
            elif line.startswith("CARTS_CPUS_RESERVATIONS"):
                CARTS_CPUS_RESERVATIONS = line.split("=")
                self.configurationJSON["Docker_Configuration"]["CARTS_CPUS_RESERVATIONS"]=CARTS_CPUS_RESERVATIONS[1]
            elif line.startswith("CARTS_RAM_LIMITS"):
                CARTS_RAM_LIMITS = line.split("=")
                self.configurationJSON["Docker_Configuration"]["CARTS_RAM_LIMITS"]=CARTS_RAM_LIMITS[1]
            elif line.startswith("CARTS_RAM_RESERVATIONS"):
                CARTS_RAM_LIMITS = line.split("=")
                self.configurationJSON["Docker_Configuration"]["CARTS_RAM_RESERVATIONS"]=CARTS_RAM_LIMITS[1]
            elif line.startswith("CARTS_REPLICAS"):
                CARTS_REPLICAS = line.split("=")
                self.configurationJSON["Docker_Configuration"]["CARTS_REPLICAS"]=CARTS_REPLICAS[1]
            # Docker configuration
            elif line.startswith("NUM_USERS"):
                NUM_USERS = line.split("=")
                self.configurationJSON["Faban_Configuration"]["NUM_USERS"]=NUM_USERS[1]
            #print("New step")
        #return configurationJSON
    
    # Reads JSON configuration file into configurationJSON - JSON dictionary.
    # Set systemConfigurationData.
    def parseJSONConfigFile(self, configurationFilePath_JSON):
        json_file = open(configurationFilePath_JSON, "r", encoding="utf-8")
        self.configurationJSON = json.load(json_file)
        json_file.close()

        # Set to SystemConfigurationData
        self.systemConfigurationData = SystemConfigurationData()
        # - Set PPTAM_Configuration.
        FABAN_IP = self.configurationJSON["PPTAM_Configuration"]["FABAN_IP"]
        JAVA_HOME_FABAN = self.configurationJSON["PPTAM_Configuration"]["JAVA_HOME_FABAN"]
        FABAN_OUTPUT_DIR = self.configurationJSON["PPTAM_Configuration"]["FABAN_OUTPUT_DIR"]
        SUT_IP = self.configurationJSON["PPTAM_Configuration"]["SUT_IP"]
        SUT_PORT = self.configurationJSON["PPTAM_Configuration"]["SUT_PORT"]
        SUT_HOSTNAME = self.configurationJSON["PPTAM_Configuration"]["SUT_HOSTNAME"]
        self.systemConfigurationData.setPPTAMConfigurationData(FABAN_IP, JAVA_HOME_FABAN, FABAN_OUTPUT_DIR, SUT_IP, SUT_PORT, SUT_HOSTNAME)
        # - Set Docker_Configuration.
        CARTS_CPUS_LIMITS = self.configurationJSON["Docker_Configuration"]["CARTS_CPUS_LIMITS"]
        CARTS_CPUS_RESERVATIONS = self.configurationJSON["Docker_Configuration"]["CARTS_CPUS_RESERVATIONS"]
        CARTS_RAM_LIMITS = self.configurationJSON["Docker_Configuration"]["CARTS_RAM_LIMITS"]
        CARTS_RAM_RESERVATIONS = self.configurationJSON["Docker_Configuration"]["CARTS_RAM_RESERVATIONS"]
        CARTS_REPLICAS = self.configurationJSON["Docker_Configuration"]["CARTS_REPLICAS"]
        self.systemConfigurationData.setDockerConfigurationData(CARTS_CPUS_LIMITS, CARTS_CPUS_RESERVATIONS, CARTS_RAM_LIMITS, CARTS_RAM_RESERVATIONS, CARTS_REPLICAS)
        # - Set Docker_Configuration.
        NUM_USERS = self.configurationJSON["Faban_Configuration"]["NUM_USERS"]
        self.systemConfigurationData.setFabanConfigurationData(NUM_USERS)    

    def getJSON_Dictionary(self):
        return self.configurationJSON

    def getSystemConfigurationData(self):
        return self.systemConfigurationData
