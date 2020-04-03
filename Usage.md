# Usage instructions

Once all tools are installed (see [Installation.md](Installation.md)), the system can be used following the following process:

1. Define test cases
2. Execute test cases
3. Extract data
4. Visualize data

In the following we describe these steps in detail.

## Define test cases

**Only** on the **driver** machine perform the following operations:

1. Execute:
   - cd ~/test_executor
   - ./benchflow.sh generate_test <NUM_USERS> <CARTS_REPLICAS> <CARTS_CPUS_LIMITS> <CARTS_CPUS_RESERVATIONS> <CARTS_RAM_LIMITS> <CARTS_RAM_RESERVATIONS>
   
Details about the parameters:
- <NUM_USERS>: No of virtual users interacting with the system
- <CARTS_REPLICAS>: No of replicas for the Carts service
- <CARTS_CPUS_LIMITS>: Max CPU Share available for the carts service
- <CARTS_CPUS_RESERVATIONS>: CPU Share available for the Carts service 
- <CARTS_RAM_LIMITS>:  Max RAM amount available for the Carts service 
- <CARTS_RAM_RESERVATIONS>: RAM amount available for the Carts service 

Example of call: 
- ./benchflow.sh generate_test 50 1 0.25 0.25 500M 500M

After such a call, a new test case folder is present in the ~/test_executor/to_execute folder. All test cases present in that folder can be executed using the instructions of the next section.

## Execute test cases

**Only** on the **driver** machine perform the following operations:

1. Make sure Faban runs executing:
   - cd ~/test_executor/faban/master/bin/
   - sudo ./startup.sh (now http://localhost:9980/ should be reachable)
2. Run tests executing:
   - cd ~/test_executor
   - Either on the console:
     - sudo ./benchflow.sh execute_tests
   - Or in the background: 
     - sudo nohup ./benchflow.sh execute_tests > log.out 2> log.err &
     - watch cat log.out log.err (to monitor the test execution like above)

You find the results in the "results" folder, in a folder named with the test id. Faban results are also available in the Faban Web Interface, usually reachable on the port 9980 of the load driver machine. 

To add Mirai as an additional load to the tested micro services, see [here](Mirai.md).

## Use another webdriver

To modify webdriver, modify the source file at the following location: ~/test_executor/faban/driver/ecsa/src/ecsa/driver/WebDriver.java

## Modify the duration of the experiment

To modify the duration of the experiment, modify the property file at the following location:
~/test_executor/templates/faban/driver/ecsa/deploy/run.xml; modify the steadystate for the experiment duration.

## Pitfalls
- benchflow.sh gives "^M: bad interpreter: No such file or directory" when executed. Please see https://stackoverflow.com/questions/17131249/how-to-solve-bad-interpreter-no-such-file-or-directory/17131267

## Extract data

After executing all tests, the executed tests are stored in the ~/test_executor/executed folder. 

**Only** on the **driver** machine perform the following operations:

1. Execute:
   - cd ~/parser
   - mix deps.get 
   - mix compile
   - mix run -e "Parser.Parser.main()"

## Visualize data

1. Open Jupyter Notebook at http://localhost:8888/ and execute the analysis.
