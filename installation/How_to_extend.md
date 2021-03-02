# How to extend PPTAM

PPTAM is a plugin-based system. The plugins are located in the `execute/plugins" folder and consist of files that are always in the order of their names. This is why certain plugins are numbered so that they are execued in the intended order.

When the user calls the `execute_test.py` script, the following steps are performed:

1. the argument `--design` is used to find the design folder;
2. the function `setup_all` is invoked in all the plugins; at this point tests are not executed, yet, therefore the parameters of `setup_all` are:
    - global_plugin_state: an array of global variables that can contain variables that need to be kept during the execution; plugins can add or remove values there;
    - current_configuration: configuration items can be read using current_configuration["name_of_configuration_item"];
    - design_path: path to the design folder;
    - test_id: the id of the test.
3. tests are run according to the tests specified in `test_plan.ini` of the current design folder. Now, the plugins are all invoked running the following methods:
    - `get_configuration_files`: retrieves an array of files that should be included in the output folder;
    - `setup`: steps to prepare the test;
    - `deploy`: steps to deploy the system under test;
    - `ready`: retrieves a boolean that confirms if the test is ready to start;
    - `before`: steps to perform before a test;
    - `run`: steps to perform the test;
    - `after`: steps to perform before a test;
    - `undeploy`: steps to undeploy the system under test;
    - `teardown`: steps to cleanup after executing a test.

    All these methods are called with the following parameters:
    - global_plugin_state: an array of global variables that can contain variables that need to be kept during the execution; plugins can add or remove values there;
    - current_configuration: configuration items can be read using current_configuration["name_of_configuration_item"];
    - output: path to the *output* folder;
    - test_id: the id of the test.

3. the function `teardown_all` is invoked in all the plugins.

To start extending PPTAM, you can copy an existing plugin and modify it, or you can start with the following template:

```
import logging

def setup_all(global_plugin_state, current_configuration, design_path, test_id):
    logging.info(f"Running setup_all")

def deploy(global_plugin_state, current_configuration, output, test_id):
    logging.info(f"Running deploy")

def before(global_plugin_state, current_configuration, output, test_id):
    logging.info(f"Running before")

def after(global_plugin_state, current_configuration, output, test_id):
    logging.info(f"Running after")

def undeploy(global_plugin_state, current_configuration, output, test_id):
    logging.info(f"Running undeploy")

def teardown_all(global_plugin_state, current_configuration, design_path, test_id):
    logging.info(f"Running teardown_all")
```

Create a new file within the `execute/plugins` folder (e.g., `plugin.py`) and try executing a test. If the logging level is at least 2, you will see the output. The folloging logging levels indicate which logging messages will be shown in the output:

- 1: all (debug, info, warning, error, and critical messages)
- 2: info, warning, error, and critical messages
- 3: warning, error, and critical messages
- 4: error, and critical messages
- 5: only critical messages