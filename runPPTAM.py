import os
from sys import platform

from generate.Parser import Parser
from generate.FileHandler import FileHandler
from generate.ReadFromFile import ReadFromFile
from generate.WriteToFile import WriteToFile
from generate.CommonMethods import CommonMethods
from generate.pptam_configuration.PPTAMConfiguration import PPTAMConfiguration
from generate.pptam_configuration.ParseConfiguration import ParseConfiguration
from generate.pptam_configuration.system_configuration.DockerConfigurationData import DockerConfigurationData
from generate.pptam_configuration.system_configuration.FabanConfigurationData import FabanConfigurationData
from generate.pptam_configuration.system_configuration.PPTAMConfigurationData import PPTAMConfigurationData
from generate.pptam_configuration.system_configuration.SystemConfigurationData import SystemConfigurationData
from run.TestExecutor import TestExecutor


# Root folder, absolute path.
rootDirectory = os.path.abspath(os.curdir)
# In case of Linux, must add / at the begining of the path.
if platform == "linux" or platform == "linux2":
    rootDirectory = "/"+rootDirectory

sysConfPath = rootDirectory+"/configuration.txt"
#sysConfPath = sysConfPath+"/configuration.json"

testExecutorOrigin = rootDirectory+"/run"
fabanDriverDestination = testExecutorOrigin+"/templates/faban"
driversDestination = testExecutorOrigin+"/drivers"

# Create necessary classes.
parser = Parser(rootDirectory)
parser.readConfiguration(sysConfPath)


print("")
print("######################################################################")
print("## Generate tests")
print("######################################################################")
print("")

parser.generateTests(testExecutorOrigin,
                     fabanDriverDestination, driversDestination)

print("")
print("######################################################################")
print("## Execute tests")
print("######################################################################")
print("")

testExecutorDestination = rootDirectory+"/run"
parseConfiguration = parser.getParseConfiguration()
testExecutor = TestExecutor(rootDirectory, parseConfiguration)
testExecutor.executeTests(testExecutorDestination)
