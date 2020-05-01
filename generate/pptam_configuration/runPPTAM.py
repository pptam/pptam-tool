import os

from BashScript import BashScript

#sysConfPath = "configuration.json"
sysConfPath = "configuration.txt"

testExecutorOrigin = "../../run"

fabanDriverDestination = "./drivers"

# os.chdir("..")
# os.chdir("..")

rootDirectory = os.path.abspath(os.curdir)

bashScript = BashScript()

print("Load configuration from "+sysConfPath+".")
bashScript.readConfiguration(sysConfPath)
bashScript.generateTests(testExecutorOrigin, fabanDriverDestination)
bashScript.executeTests(rootDirectory)
