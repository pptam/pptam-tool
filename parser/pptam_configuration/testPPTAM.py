from BashScript import BashScript

#sysConfPath = "configuration.json"
sysConfPath = "configuration.txt"

bashScript = BashScript()

bashScript.readConfiguration(sysConfPath)
bashScript.generateTests()

def generate_tests(confFileName):
	print("Load configuration from "+confFileName+".")
	bashScript.readConfiguration(confFileName)
	bashScript.generateTests()
	