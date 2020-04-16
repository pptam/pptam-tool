from BashScript import BashScript

#sysConfPath = "configuration.json"
sysConfPath = "configuration.txt"

testExecutorOrigin = "../../test_executor"

fabanDriverDestination = "./drivers"

bashScript = BashScript()

bashScript.readConfiguration(sysConfPath)
bashScript.generateTests(testExecutorOrigin, fabanDriverDestination)
bashScript.executeTests()

def generate_tests(confFileName):
	print("Load configuration from "+confFileName+".")
	bashScript.readConfiguration(confFileName)
	bashScript.generateTests()
	