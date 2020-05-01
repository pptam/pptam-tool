# Holds the full system configuration.

from generate.pptam_configuration.system_configuration.DockerConfigurationData import DockerConfigurationData
from generate.pptam_configuration.system_configuration.FabanConfigurationData import FabanConfigurationData
from generate.pptam_configuration.system_configuration.PPTAMConfigurationData import PPTAMConfigurationData


class SystemConfigurationData():
    pptamConfigurationData = None
    dockerConfigurationData = None
    fabanConfigurationData = None

    def getPPTAMConfigurationData(self):
        return self.pptamConfigurationData

    def getDockerConfigurationData(self):
        return self.dockerConfigurationData

    def getFabanConfigurationData(self):
        return self.fabanConfigurationData

    def setPPTAMConfigurationData(self, FABAN_IP, JAVA_HOME_FABAN, FABAN_OUTPUT_DIR, SUT_IP, SUT_PORT, SUT_HOSTNAME, preExecExternalCommands, postExecExternalCommands):
        # print("preExecExternalCommands:")
        # print(preExecExternalCommands)
        # print("postExecExternalCommands:")
        # print(postExecExternalCommands)
        self.pptamConfigurationData = PPTAMConfigurationData(
            FABAN_IP, JAVA_HOME_FABAN, FABAN_OUTPUT_DIR, SUT_IP, SUT_PORT, SUT_HOSTNAME, preExecExternalCommands, postExecExternalCommands)

    def setDockerConfigurationData(self, CARTS_CPUS_LIMITS, CARTS_CPUS_RESERVATIONS, CARTS_RAM_LIMITS, CARTS_RAM_RESERVATIONS, CARTS_REPLICAS):
        self.dockerConfigurationData = DockerConfigurationData(
            CARTS_CPUS_LIMITS, CARTS_CPUS_RESERVATIONS, CARTS_RAM_LIMITS, CARTS_RAM_RESERVATIONS, CARTS_REPLICAS)

    def setFabanConfigurationData(self, NUM_USERS):
        self.fabanConfigurationData = FabanConfigurationData(NUM_USERS)
