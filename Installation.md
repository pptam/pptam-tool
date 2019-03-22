# Installation instructions

The installation assumes the following setup:

- One machine called “driver”: this machine contains most of our tools to control the experiment and to analyze the results.
- One machine called “test”: this machine contains just the operating system and docker, which will be part of the swarm controlled by the driver.

To setup this environment, it is possible to use real machines or to simulate the setup using virtual machines. In the following description we use [Oracle VM VirtualBox](https://www.oracle.com/technetwork/server-storage/virtualbox/downloads/index.html), so that pptam can be installed and used on one machine, e.g., a laptop, for testing purposes.

The installation is grouped into the following parts:

- Part 1: install the test executor;
- Part 2: install the tools to collect, analyze, and visualize data.
   
## Part 1: install the test executor

Start [Oracle VM VirtualBox](https://www.oracle.com/technetwork/server-storage/virtualbox/downloads/index.html) and create two machines for Linux/Ubuntu (64 bit). One called “driver”, one called “test”. Setup the network configuration for both VMs to use two network cards:

- one set to “NAT” and
- one set to “Host-only Adapter”.

On **both** machines perform the following operations:

1. Upon start, install both VMs using the [ubuntu-18.04.1.0-live-server-amd64.iso](http://releases.ubuntu.com/18.04/)
2. During setup, while the network configuration is displayed, configure both machines as follows (this configuration is later stored in /etc/cloud/cloud.cfg.d/50-curtin-networking.cfg. If you need to change it and want to modify that file, you have to execute sudo cloud-init clean && sudo cloud-init init && sudo netplan apply):
   - Let the first network card as it is (initialized through DHCP, with a valid IP address displayed during setup; enable IPv6 DHCP in case there is no valid address for IPv4)
   - Manually configure the second network card to an IPv4 address:
     - Configuration of the driver VM: 
       - Subnet: 192.168.2.0/24
       - Address: 192.168.2.1
     - Configuration of the test VM:
       - Subnet: 192.168.2.0/24
       - Address: 192.168.2.2
3. Also during setup, configure a user (I used username "user" and password "user", but you can take any user with any password).
4. After setup, start both machines and execute:
   - sudo -i (to execute all following commands as sudo)
   - apt update -y
   - apt upgrade -y
   - apt install -y apt-transport-https ca-certificates curl lxc iptables
   - curl -sSL https://get.docker.com/ | sh
   - usermod -aG docker user
   - apt install -y nano unzip ant inetutils-ping
   - apt-get install -y openjdk-8-jdk
   - Add to /etc/environment:
     - JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/"
   - Add to /etc/hosts:
     - 192.168.2.1 driver
     - 192.168.2.2 test

**Only** on the **driver** machine perform the following operations:

1. Open the settings of the virtual machine, open the network tab, for adapter 1, open the advanced settings and open the port forwarding window. Define the following rules:
   - (Optional) SSH (this allows you to use a comfortable SSH client to interact with the virtual machines, e.g., allowing you to copy/paste instructions into the client): 
     - Name: SSH
     - Protocol: TCP
     - Host IP: (empty)
     - Host Port: 2222 
     - Guest IP: (empty)
     - Guest Port: 22
   - Faban (this allows you to see the testing results):
     - Name: Faban
     - Protocol: TCP
     - Host IP: (empty)
     - Host Port: 9980
     - Guest IP: (empty)
     - Guest Port: 9980
   - Jupyter (this allows you to see the analysis results):
     - Name: Jupyter
     - Protocol: TCP
     - Host IP: (empty)
     - Host Port: 8888
     - Guest IP: (empty)
     - Guest Port: 8888
2. Run the machine, zip the [test_executor](test_executor) folder to test_exector.zip and copy it into the home of the current user (I used [Cyberduck](https://cyberduck.io/)). The test executor is adapted from Alberto Avritzer, Vincenzo Ferme, Andrea Janes, Barbara Russo, Henning Schulz, & André van Hoorn. (2018). A Quantitative Approach for the Assessment of Microservice Architecture Deployment Alternatives by Automated Performance Testing [Data set]. Zenodo. http://doi.org/10.5281/zenodo.1256488
3. Then within the driver machine execute:
   - cd ~
   - unzip test_executor.zip
   - sudo docker swarm init --advertise-addr 192.168.2.1
4. Moreover, to prepare the test execution, execute:
   - cd ~/test_executor
   - mkdir drivers/tmp
5. Modify ~/test_executor/config.properties to include the current configuration:
   - faban.ip=192.168.2.1
   - sut.ip=192.168.2.2
   - sut.hostname=test
   - java.home=\/usr\/lib\/jvm\/java-8-openjdk-amd64\/

**Only** on the **test** machine perform the following operations:

1. Open the settings of the virtual machine, open the network tab, for adapter 1, open the advanced settings and open the port forwarding window. Define the following rules:
   - (Optional) SSH (this allows you to use a comfortable SSH client to interact with the virtual machines, e.g., allowing you to copy/paste instructions into the client): 
     - Name: SSH
     - Protocol: TCP
     - Host IP: (empty)
     - Host Port: 2223 
     - Guest IP: (empty)
     - Guest Port: 22
2. Execute:
   - sudo (command that swarm init executed above recommends to execute)

At this point, the machines are ready to perform tests and to collect the results. As a next step, we need to install the necessary tools to analyze and visualize the data.

## Part 2: install the tools to collect, analyze, and visualize data

### Install InfluxDB (to collect the necessary data to generate the operational profile)

**Only** on the **driver** machine perform the following operations:

1. Execute:
   - curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
   - source /etc/lsb-release
   - echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
   - sudo apt update && sudo apt install -y influxdb
   - sudo service influxdb start

### Install Elixir and the parser (to extract and prepare the collected data)

**Only** on the **driver** machine perform the following operations:

1. Execute:
   - cd /tmp
   - wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb && sudo dpkg -i    - erlang-solutions_1.0_all.deb
   - sudo apt update && sudo apt install -y esl-erlang elixir
   - mix local.hex --force
   - mix local.rebar --force
2. Then, zip the [parser](parser) folder to parser.zip and copy it into the home of the current user (I used [Cyberduck](https://cyberduck.io/)). 

### Install Jupyter and the Jupyter notebook file (to analyze the collected data)

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
   - c.NotebookApp.ip = '*'
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


