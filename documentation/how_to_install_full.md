# Full installation

Installing PPTAM on two machines, or installing it in the cloud requires that you have two machines that can reach each other over the network. This usually requires configuration that we cannot foresee, therefore we cannot build an installer for it. Therefore, we can here only give guidelines how to proceed:

1. Setup two machines (which we call "driver" and "testbed") so that they can reach each other on a network. 
   - Driver is just "driving" the experiment and can be relatively small, e.g., 4 Cores, 16GB RAM, 40GB hard disk space.
   - Testbed needs to be as powerful as needed to execute the software under test. Programs like [Trainticket](https://github.com/FudanSELab/train-ticket), for example, require 24GB of RAM and 50GB of hard disk space.
   
   Make sure that the following ports are open on the testbed:
   - TCP 2375
   - TCP 2376
   - TCP 2377
   - TCP and UDP 7946
   - UDP 4789

2. Install Ubuntu 18.04.4 LTS on both machines.
3. Let's start with the driver:
   - Execute the steps we perform for the installation using virtual machines ([installation/scripts/install_both.sh](scripts/install_both.sh)), but adapt them to your configuration: 
      - use your IP addresses;
      - use your machine names;
      - change the user "vagrant" to the user you are using;
   - Execute the *driver-specific* steps for the driver we perform for the installation using virtual machines ([installation/scripts/install_driver.sh](scripts/install_driver.sh)), but adapt them to your configuration: 
      - use your IP addresses;
      - use your machine names;
      - change the user "vagrant" to the user you are using;
      - change /home/vagrant to your home directory;
      - when creating a Docker swarm, `install_driver.sh` saves the join token in `/vagrant/.join-token-worker` so that `install_testbed.sh` can pick it up from there. When installing Docker swarm on two real machines, you can skip saving the token and execute the join instruction Docker displays when creating the swarm within the driver;
      - keep in mind that the /vagrant folder within the Vagrant installation scripts is the `installation` folder of the PPTAM repository. Therefore, when in the installation script we copy files from `/vagrant`, you need to copy them from the `installation` folder.
   - Execute the *testbed-specific* steps for the driver we perform for the installation using virtual machines ([installation/scripts/install_testbed.sh](scripts/install_testbed.sh)), but adapt them to your configuration: 
      - use the Docker swarm join instruction that you got when installing the driver;
      - change the user "vagrant" to the user you are using;
      - change /home/vagrant to your home directory;