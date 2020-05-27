from os import path
import os
import json
from datetime import datetime
import uuid

######################################################################
# Creates a test plan.
# This is a blue print for generation of tests.
# After this script generates a number of tests with default values for parameters, feel free to change them.
######################################################################
# How many tests?
NUMBER_OF_TESTS = 5
# If the file exists, new tests will be simply added to the end of the list.
testPlanFile = "../configuration/testPlan.json"

# Function intends to concatenate lists with strings, strings with strings, lists with lists, and strings with lists.
def updateOldValue(oldValue, valueToAdd):  
    if isinstance(oldValue, (list, tuple)):
        # Remove commas from the list.
        newList = []
        for li in oldValue:
            li = li.replace(',', '')
            newList.append(li)
        if isinstance(valueToAdd, str):
            valueToAdd.replace(',', '')
            if valueToAdd not in newList:
                newList.insert(0, valueToAdd)
            return oldValue
        if isinstance(valueToAdd, (list, tuple)):
            newList1 = []
            for li in valueToAdd:
                li = li.replace(',', '')
                newList1.append(li)
            if (newList1 == newList):
                return newList
            return newList1+newList
    else:
        if isinstance(oldValue, str):
            oldValue.replace(',', '')
            if isinstance(valueToAdd, str):
                valueToAdd.replace(',', '')
                if (oldValue == valueToAdd):
                    return oldValue
                return oldValue+valueToAdd
            elif isinstance(valueToAdd, (list, tuple)):
                # Remove comma
                newList = []
                for li in valueToAdd:
                    li = li.replace(',', '')
                    newList.append(li)
                if oldValue not in newList: 
                    newList.insert(0, oldValue)
                return newList  
    print(f"Firtst param is of type {type(oldValue)}, and the second param is of type {type(valueToAdd)} - return the second param")
    return valueToAdd

# Load configuration.
configuration_file_path = "../configuration/configuration.json"

if not path.exists(configuration_file_path):
    logging.fatal(f"Cannot find the configuration file {configuration_file_path}.")
    quit()
configuration = None
with open(configuration_file_path, "r") as f:
    configuration = json.load(f)["Configuration"]
    
# For every test generate a set of configuration parameters (based on the configuration file).
# Get place holders for the configuration.
deploymentOpt = configuration["deployment"] 
executionAndMeasurementOpt = configuration["execution_and_measurement"]
sutOpt = configuration["sut"]

# Handle deployment place holders.
deploymentConf = None
with open("../configuration/thirdParty/deployment.json", "r") as f:
    deploymentConf = json.load(f)[deploymentOpt]
    
# Handle execution and measurement place holders.
executionAndMeasurementConf = None
with open("../configuration/thirdParty/executionAndMeasurement.json", "r") as f:
    executionAndMeasurementConf = json.load(f)[executionAndMeasurementOpt]

# Handle system under test place holders.
sutConf = None
with open("../configuration/thirdParty/sut.json", "r") as f:
    sutConf = json.load(f)[sutOpt]

# Have default values.
testPlanDict = {}

testInstance = {}

while(NUMBER_OF_TESTS>0):
    NUMBER_OF_TESTS = NUMBER_OF_TESTS-1
    testInstance.clear()
    # Generate random test ID.
    now = datetime.now()
    test_id = configuration["test_case_prefix"] + "-" + \
        now.strftime("%Y%m%d%H%M%S") + "-" + str(uuid.uuid4())[:8]
    #print("Test "+test_id+" - start plan.")
    
    testInstance["TEST_ID"] = test_id
    
    # Deployment place holders.
    for paramKey in deploymentConf:
        #print(f"{testPlanDict[test_id][paramKey] = confParam[paramKey]}")
        if paramKey in testInstance:
            #print(f"{paramKey} already exists.")
            newValue = updateOldValue(testInstance[paramKey], deploymentConf[paramKey])
            testInstance[paramKey] = newValue
        else:
            testInstance[paramKey] = deploymentConf[paramKey]
    
    # Execution and measurement place holders.
    for paramKey in executionAndMeasurementConf:
        #print(f"{testPlanDict[test_id][paramKey] = executionAndMeasurementConf[paramKey]}")
        if paramKey in testInstance:
            #print(f"{paramKey} already exists.")
            newValue = updateOldValue(testInstance[paramKey], executionAndMeasurementConf[paramKey])
            testInstance[paramKey] = newValue
        else:
             testInstance[paramKey] = executionAndMeasurementConf[paramKey]
    
    # System under test place holders.
    for paramKey in sutConf:
        #print(f"{testPlanDict[test_id][paramKey] = sutConf[paramKey]}")
        if paramKey in testInstance:
            newValue = updateOldValue(testInstance[paramKey], sutConf[paramKey])
            testInstance[paramKey] = newValue
        else:
            testInstance[paramKey] = sutConf[paramKey]
    
    testPlanDict[test_id] = testInstance
    print("Test "+test_id+" - test plan created.")

# If the previous plan already exists.
if os.path.isfile(testPlanFile): 
    print("--- Update the existing dictionary.")
    
    with open(testPlanFile, 'r') as f:
        # Update with the already existing test plan.
        oldDictionary = json.load(f)
        testPlanDict.update(oldDictionary)

with open(testPlanFile, 'w') as f:
        json.dump(testPlanDict, f, sort_keys=True, indent=4, separators=(',', ': '))
# Write a script that creates tests based on the test plan.
# createTestPlan will generate a random ID.
# Change createTest to read testPlan instead of the configuration.