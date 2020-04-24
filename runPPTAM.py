import os
from sys import platform

from configurationParser.Parser import Parser
from configurationParser.FileHandler import FileHandler
from configurationParser.ReadFromFile import ReadFromFile
from configurationParser.WriteToFile import WriteToFile
from configurationParser.CommonMethods import CommonMethods
from configurationParser.pptam_configuration.PPTAMConfiguration import PPTAMConfiguration
from configurationParser.pptam_configuration.ParseConfiguration import ParseConfiguration
from configurationParser.pptam_configuration.system_configuration.DockerConfigurationData import DockerConfigurationData
from configurationParser.pptam_configuration.system_configuration.FabanConfigurationData import FabanConfigurationData
from configurationParser.pptam_configuration.system_configuration.PPTAMConfigurationData import PPTAMConfigurationData
from configurationParser.pptam_configuration.system_configuration.SystemConfigurationData import SystemConfigurationData
from test_executor.TestExecutor import TestExecutor


# Root folder, absolute path.
rootDirectory = os.path.abspath(os.curdir)
# In case of Linux, must add / at the begining of the path.
if platform == "linux" or platform == "linux2":
    rootDirectory = "/"+rootDirectory
    
sysConfPath = rootDirectory+"/configuration.txt"
#sysConfPath = sysConfPath+"/configuration.json"

testExecutorOrigin = rootDirectory+"/test_executor"
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

parser.generateTests(testExecutorOrigin, fabanDriverDestination, driversDestination)

print("")
print("######################################################################")
print("## Execute tests")
print("######################################################################")
print("")

testExecutorDestination = rootDirectory+"/test_executor"
parseConfiguration = parser.getParseConfiguration()
testExecutor = TestExecutor(rootDirectory, parseConfiguration)
testExecutor.executeTests(testExecutorDestination)