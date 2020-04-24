from configurationParser.pptam_configuration.PPTAMConfiguration import PPTAMConfiguration

# Manage parsing of the input configuration. 
# Manage test generation.

class Parser: 
    pptamConfiguration = None
    # Saves file name.
    def __init__(self, rootDirectory): 
        print("Parser created.")
        print("Root folder = " + rootDirectory)    
    
    def readConfiguration(self, sysConfPath):
        print("Configuration file = " + sysConfPath)
        self.pptamConfiguration = PPTAMConfiguration()
        self.pptamConfiguration.readConfiguration(sysConfPath)
        
    def generateTests(self, testExecutorOrigin, fabanDriverDestination):
        print("test_executor folder = " + testExecutorOrigin)
        print("Faban driver temp destination folder = " + testExecutorOrigin)
        self.pptamConfiguration.generateTests(testExecutorOrigin, fabanDriverDestination)
    
    def getParseConfiguration(self):
        return self.pptamConfiguration.getParseConfiguration()
