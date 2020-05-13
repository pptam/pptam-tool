# Installation instructions

**Only** on the **driver** machine perform the following operations:

1. Run the machine, zip the [test_executor](test_executor) folder to test_exector.zip and copy it into the home of the current user (I used [Cyberduck](https://cyberduck.io/)). The test executor is adapted from Alberto Avritzer, Vincenzo Ferme, Andrea Janes, Barbara Russo, Henning Schulz, & André van Hoorn. (2018). A Quantitative Approach for the Assessment of Microservice Architecture Deployment Alternatives by Automated Performance Testing [Data set]. Zenodo. http://doi.org/10.5281/zenodo.1256488
2. Then within the driver machine execute:
   - cd ~
   - unzip test_executor.zip
   - sudo docker swarm init --advertise-addr 192.168.2.1
3. Moreover, to prepare the test execution, execute:
   - cd ~/test_executor
   - mkdir drivers/tmp
4. Modify ~/test_executor/config.properties to include the current configuration:
   - faban.ip=192.168.2.1
   - sut.ip=192.168.2.2
   - sut.hostname=test
   - java.home=\/usr\/lib\/jvm\/java-8-openjdk-amd64\/
5. Make sure the following empty folders exist
   - mkdir ~/test_executor/faban/master/common/endorsed
   - mkdir ~/test_executor/executed
   - mkdir ~/test_executor/to_execute
   - mkdir ~/test_executor/drivers
   - mkdir ~/test_executor/drivers/tmp
   - mkdir ~/test_executor/faban/master/temp

**Only** on the **test** machine perform the following operations:

1. Execute:
   - sudo (command that swarm init executed above recommends to execute)

At this point, the machines are ready to perform tests and to collect the results. As a next step, we need to install the necessary tools to analyze and visualize the data.

## Part 2: install the tools to collect, analyze, and visualize data

### Optional: Install InfluxDB (to collect the necessary data to generate the operational profile)

**Only** on the **driver** machine perform the following operations:

1. Execute:
   - curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
   - source /etc/lsb-release
   - echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} \${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
   - sudo apt update && sudo apt install -y influxdb
   - sudo service influxdb start

### Deprecated: Install Elixir and the parser (to extract and prepare the collected data)

**Only** on the **driver** machine perform the following operations:

1. Execute:
   - cd /tmp
   - wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb && sudo dpkg -i - erlang-solutions_1.0_all.deb
   - sudo apt update && sudo apt install -y esl-erlang elixir
   - mix local.hex --force
   - mix local.rebar --force
2. Then, zip the [parser](parser) folder to parser.zip and copy it into the home of the current user (I used [Cyberduck](https://cyberduck.io/)).

### Optional: Install Jupyter and the Jupyter notebook file (to analyze the collected data)

**Only** on the **driver** machine perform the following operations:

1. Execute:
   - cd /tmp
   - curl -O https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh
   - bash Anaconda3-5.3.1-Linux-x86_64.sh (answer yes/ENTER to everything, except to install VS Code)
   - source ~/.bashrc
   - cd ~
   - jupyter notebook --generate-config
   - jupyter notebook password (Define your jupyter password, or type ENTER twice for an empty password)
2. Update the following values in/home/user/.jupyter/jupyter_notebook_config.py:
   - c.NotebookApp.allow_remote_access = True
   - c.NotebookApp.ip = '\*'
   - c.NotebookApp.open_browser = False
3. Then, execute:
   - conda install -c r r-essentials (answer y)
   - conda deactivate
   - mkdir ~/notebooks
   - cd ~/notebooks
   - conda create -n pptam python anaconda r-essentials (see https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
   - conda activate pptam
   - jupyter notebook (now http://localhost:8888/ should be reachable)
4. Then, copy the files of the [analyzer](analyzer) folder into the notebooks folder created above (I used [Cyberduck](https://cyberduck.io/)).
