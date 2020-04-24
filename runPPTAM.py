import os

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
sysConfPath = rootDirectory+"/configuration.txt"
#sysConfPath = sysConfPath+"/configuration.json"

testExecutorOrigin = rootDirectory+"/test_executor"
fabanDriverDestination = rootDirectory+"/configurationParser/pptam_configuration/drivers"

# Create necessary classes.
parser = Parser(rootDirectory)
parser.readConfiguration(sysConfPath)


print("")
print("######################################################################")
print("## Generate tests")
print("######################################################################")
print("")

parser.generateTests(testExecutorOrigin, fabanDriverDestination)

print("")
print("######################################################################")
print("## Execute tests")
print("######################################################################")
print("")

testExecutorDestination = rootDirectory+"/test_executor"
parseConfiguration = parser.getParseConfiguration()
testExecutor = TestExecutor(rootDirectory, parseConfiguration)
testExecutor.executeTests(testExecutorDestination)