# How to use PPTAM

## Configuration
PPTAM helps to you to conduct load tests. We use the following terminology:

 - Test design: describes the configuration of the test and all the necessary input to conduct a load test;
 - Test plan: describes the various tests to execute;
 - Test execution: executes a test design and stores the result; and
 - Test analysis: analyzes the output of one and more test results.

 Therefore, the PPTAM repository contains various design folders, some of them are examples:

 - design_website: a super simple test design that just performs a load test of a remote web site (without installing it on the testbed). 
 - design_jsonserver: a json server that is deployed on the testbed and then tested.

 Typically a design folder contains:
   - configuration.ini: a file that contains all configuration parameters to conduct the load test. Please refer to the file itself for the configuration parameters.
   - docker-compose.yml: a [https://docs.docker.com/compose/](Docker compose) file to deploy the system under test on the testbed. 
   - locustfile.py: load tests are conducted using [https://locust.io](locust.io), which requires a [https://docs.locust.io/en/stable/writing-a-locustfile.html](locustfile.py) to describes how to interact with the system under test. This one just calles several pages of the website we are testing.
   - test_plan.ini: describes the tests to perform.
   
Test_plan.ini contains various sections that start with "Test", each section describes one test. For each such section, PPTAM executes a test considering configuration.ini as the base configuration and using the settings within test_plan.ini for the specific test. That means that a test section can overwrite any setting in configuration.ini. For example: configuration.ini contains the setting "RUN_TIME_IN_SECONDS = 60". Within test_plan.ini one could define a section [Test1] that overwrites this setting specifying "RUN_TIME_IN_SECONDS = 120". That means that *for that single test* that setting is changed. Let's have a look at the following example:

```
[DEFAULT]
SECONDS_TO_WAIT_BEFORE_SETUP=10

[Test1]
LOAD=10
RUN_TIME_IN_SECONDS=60

[Test2]
LOAD=20
RUN_TIME_IN_SECONDS=120
```

In this case, test_plan.ini overwrites SECONDS_TO_WAIT_BEFORE_SETUP for all tests. Then, it specifies two tests: one with a load of 10 users, running for 60 seconds, and one with a load of 20 users, running for 120 seconds.

## Execution

Once a test design is present, its possible to execute tests using the `execute_test.py` script within the `execute` folder. This script accepts three arguments:

* --design: the path to the design folder;
* --logging: the logging level from 1 (everything) to 5 (nothing), default is 2;
* --overwrite: if present, overwrites existing test cases, default is false.

An example call could be:

- cd ~/pptam-tool/execute
- `su -u vagrant ./execute_test.py --design=../design_jsonserver_vagrant --logging=1 --overwrite`

This call would execute the tests present in the json server design folder, log everything and overwrite existing test cases (if present).

If a file `arguments.ini` is present in the execute folder, the parameters indicated in that configuration file will be read, not those provided on the command line. It has the following format:

```
[ARGUMENTS]
OVERWRITE=1
DESIGN=../design_trainticket
LOGGING=1
````

## Analysis

The results of an experiment will be written in the `execute/executed` folder. The folder name have the format `yyyyMMddHHmm-prefix-test`, where the single parts have the following meaning:

- yyyyMMddHHmm is the current date and time, e.g., 202102111435 means 11th of February, 2021 at 2:35pm;
- prefix is the text configured in the setting TEST_CASE_PREFIX;
- test is the name of the test provided within square brackets in test_plan.ini (e.g., test1);

**Do not choose a very long prefix and test name: the deployments using Docker also consider these settings and Docker has a maximimal length for container names**

Typically, after performing a test, you will find the following files in the results folder:

- configuration.ini: A copy of all settings used in this test (the merge of configuration.ini and the settings overwritten in the test plan for this specific test);
- locustfile.log: the logfile of locust, useful for debugging when setting up a new test design;
- locustfile.out: the commandline of the locust execution, obtained redirecting standard output and standard error;
- locustfile.py: the used locust file;
- result_failures.csv: the list of errors while executing the load test;
- result_stats_history.csv: the response times while executing the load test;
- result_stats.csv: the summary of the response times of the load test;
- other files that the different plugins present in the `execute/plugins` folder generated.