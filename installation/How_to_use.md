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
   - configuration.ini: a file that contains all configuration parameters to conduct the load test. Please see below the section "configuration parameters" for the explaination of the single parameters.
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

### Configuration parameters

`configuration.ini` contains the following parameters:

- ENABLED_PLUGINS: this parameter decides which plugins to execute. Currently the following plugins are available:

  - cleanup_docker.py: deletes old Docker containers and restarts Docker *before* a test;
  - deploy_docker.py: deploys the system under test using the provided `docker-compose.yml`;
  - analyze_portainer.py: deploys [Portainer](https://www.portainer.io), for debugging;
  - deploy_files.py: deploys optional additional files to the execution folder;
  - measure_docker_stats.py: measures the system under test collecting [Docker stats](https://docs.docker.com/engine/reference/commandline/stats/);
  - measure_jaeger.py: collects [Jaeger tracing](https://www.jaegertracing.io) data.
  - load_test_locust.py: executes a [Locust](https://locust.io) load test;
  - test_deployment.py: tests if the application is deployed correctly checking for a specific container.

  This parameter has to be set listing the plugins to use, separated by a space, e.g., deploy_docker test_deployment load_test_locust. **The plugins are executed in the order they are set in the parameter**.

- PROJECT_NAME: Name of the current project
- TEST_SET_NAME: (Useful to group tests into test sets) Name of the test set
- TEST_CASE_PREFIX: Prefix to add to every test; useful to distinguish test sets
- SECONDS_TO_WAIT_BEFORE_SETUP: Seconds to wait before starting the phase 'setup'
- SECONDS_TO_WAIT_BEFORE_DEPLOY: Seconds to wait before starting the phase 'deploy'
- SECONDS_TO_WAIT_BEFORE_BEFORE: Seconds to wait before starting the phase 'before'
- SECONDS_TO_WAIT_BEFORE_RUN: Seconds to wait before starting the phase 'run'
- SECONDS_TO_WAIT_BEFORE_AFTER : Seconds to wait before starting the phase 'after'
- SECONDS_TO_WAIT_BEFORE_UNDEPLOY: Seconds to wait before starting the phase 'undeploy'
- SECONDS_TO_WAIT_BEFORE_TEARDOWN: Seconds to wait before starting the phase 'teardown'
- ENABLED: Set to 0 to disable this test

The following settings are used if the `load_test_locust.py` plugin is used:
- LOCUST_HOST_URL: the url that locus uses to conduct performance tests.
- LOAD: Load to generate for a test. This value should be specified in a test plan.
- SPAWN_RATE_PER_SECOND: Speed at which new users are launched.
- RUN_TIME_IN_SECONDS: Duration of the overall test.

The following settings are used if the `0_deploy_docker.py` plugin is used:
- DOCKER_NODE_NAME: the node on which the system under test (SUT) must be deployed.
- DOCKER_WAITING_FOR_DEPLOYMENT_IN_SECONDS: seconds to wait till a system is deployed.
- DOCKER_WAITING_FOR_UNDEPLOYMENT_IN_SECONDS: seconds to wait till a system is undeployed.

The following settings are used if the `8_measure_docker_stats.py` plugin is used:
- DOCKER_STATS_HOSTNAME: host to contact to obtain docker stats.
- DOCKER_STATS_CONTAINERS: either choose 'all' or indicate the containers, separated by a space.
- DOCKER_STATS_VERBOSE: use 0 or 1 to disable or enable verbose mode.
- DOCKER_STATS_SLEEP_BETWEEN_STATS_READING_IN_SECONDS: time to wait between reading stats.

The following settings are used if the `9_measure_jaeger.py` plugin is used:
- JAEGER_HOST_URL: host to contact to obtain Jaeger traces.
- JAEGER_SERVICES: either choose 'all' or indicate the services, separated by a space.
- JAEGER_TEST_IF_SERVICE_IS_PRESENT: specify a service that should be present to start collecting Jaeger data

The following settings are used if the `test_deployment.py` plugin is used:
- DOCKER_TEST_HOSTNAME: host to contact to contact Docker
- DOCKER_TEST_IF_IMAGE_IS_PRESENT: either choose 'all' or indicate the services, separated by a space.

The following settings are used if the `2_deploy_files.py` plugin is used:
- FILES_TO_INCLUDE: the list of files, separated by space, to include in the output folder

### Typical setups

If you want to load test an application that is *already deployed*, have a look at the `design_website` folder. You do not need to deploy the system under test using docker and you might only need the `load_test_locust.py` plugin. If you need want to deploy the system under test, have a look at the `design_jsonserver`.

## Execution

Once a test design is present, its possible to execute tests using the `execute_test.py` script within the `execute` folder. This script accepts the following arguments:

* design_folder: the path to the design folder;
* --logging: the logging level from 1 (everything) to 5 (nothing), default is 1;

An example call could be:

- cd ~/pptam-tool/execute
- `./execute_test.py ../design_jsonserver_vagrant --logging=1`

Depending on your configuration, you need to use `sudo` to execute tests. This call would execute the tests present in the json server design folder, log everything and overwrite existing test cases (if present).

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