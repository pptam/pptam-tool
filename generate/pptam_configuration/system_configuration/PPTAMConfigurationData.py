# Configuration of the PPTAM execution parameters.

class PPTAMConfigurationData():
	# The ip of the server on which Faban runs (load driver machine).
	fabanIP=None
	# The path to Java for Faban, set once only when installing the system.
	javaHomeFaban=None
	# The path where Faban should write the results, set once only when installing the system.
	fabanOutputDir=None
	# System under test IP (SUT_IP): the ip of the server on which the system under test is going to be deployed (sut machine)
	sutIP=None
	# System under test port (SUT_PORT): the port of the sut (the default one is 80)
	sutPort=None
	# System under test host name (SUT_HOSTNAME): the hostname of the server on which the system under test is going to be deployed (sut machine
	sutHostname=None
	# The list of commands to execute before tests.
	preExecExternalCommands = None
	# The list of commands to execute after tests.
	postExecExternalCommands = None
	
	def __init__(self, FABAN_IP, JAVA_HOME_FABAN, FABAN_OUTPUT_DIR, SUT_IP, SUT_PORT, SUT_HOSTNAME, preExec, postExec): 
		self.fabanIP=FABAN_IP
		self.javaHomeFaban=JAVA_HOME_FABAN
		self.fabanOutputDir=FABAN_OUTPUT_DIR
		self.sutIP=SUT_IP
		self.sutPort=SUT_PORT
		self.sutHostname=SUT_HOSTNAME
		self.preExecExternalCommands=preExec
		self.postExecExternalCommands=postExec
		
		#print("Pre execution commands:")
		#print(preExec)
		#for cm in preExec:
			#print(cm)	
		
		#print("Post execution commands:")
		#print(postExec)
		#for cm in postExec:
			#print(cm)	

	def getFabanIP(self):
		return self.fabanIP
	def getJavaHomeFaban(self):
		return self.javaHomeFaban
	def getfabanOutputDir(self):
		return self.fabanOutputDir
	def getSutIP(self):
		return self.sutIP
	def getSutPort(self):
		return self.sutPort
	def getSutHostname(self):
		return self.sutHostname
	def getPreExecExternalCommands(self):
		return self.preExecExternalCommands
	def getPostExecExternalCommands(self):
		return self.postExecExternalCommands