# Use of PPTAM

This description explains how to carry out tests using PPTAM. PPTAM allows you to carry out production and performance testing, therefore it is necessary to:

1. define the software under test (SUT);
2. define the tests to carry out;
3. execute the tests; and
4. analyze the results.

## Defining the software under test

The software under test needs to be deployed on the testbed machine. For this purpose, the software to deploy has to be defined within `/create/templates/deployment_descriptor/template/docker-compose.yml`.

If you need to define parameters within the `docker-compose.yml` file, these parameters can be called `${PARAMETER_NAME}` and defined within `/configuration/configuration.txt`. They will be replaced when tests are defined.

The tests carried out by [Faban](http://faban.org) have to be defined in `/create/templates/faban/driver/pptam/src/pptam/driver/WebDriver.java`. Refer to [Faban](http://faban.org) to see how to define a web driver. Also within `WebDriver.java`, all parameters present in `/configuration/configuration.txt` in the form `${PARAMETER_NAME}` will be replaced.

## Define the tests to carry out

1. Verify the file `/configuration/configuration.txt` to see if all parameters are correct. Please refer to the configuration file to understand the meaning of each parameter.
2. Open a terminal window and carry out the following commands within the project directory:

   - `cd create`
   - `./create_test.sh`.

3. A test case is created and added to the folder `/create/to_execute`.

## Execute the tests

1. Open a terminal window and carry out the following commands within the project directory:

   - `cd execute`
   - `./run_faban.sh`
   - `./execute_test.sh`

During the test, Faban should be reachable at `http://(name of the driver machine):9980` as shown [here](./attachments/faban.png).

2. The command runs the testing framework Faban and executes all tests prepared in `/execute/to_execute`. Once the tests are executed, they are moved into `/execute/executed`.

## Analyze the results

1. Open a terminal window and carry out the following commands within the project directory:

   - `cd analyze`
   - `./run_jupyter_notebook.sh`

The command changes directory to the folder ./notebooks and runs Jupiter Notebook, reachable at `http://(name of the driver machine):8888` as shown [here](./attachments/jupyter.png).

## Troubleshooting

If something goes wrong, these things should be checked:

- Is the configuration file correct?
- Is Faban running?
- Is the second machine, the testbed reachable?
- Is Docker running on both machines?
- Is enough hard disk space available on the testbed machine?
