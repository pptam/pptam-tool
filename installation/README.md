# Installation

PPTAM is supposed to be installed on two Linux machines:

- The "driver": a machine to **control** the experiment.
- The "testbed": a machine to **execute** the experiment.

The installation requires to setup both machines so that they can reach each other on a network and install [Docker](https://www.docker.com) on both machines. Only on the driver, you have to install PPTAM to control and visualize the output of experiments.

To make it easier to try out and play with PPTAM, we foresee two types of installation:

- An installation using two **virtual** machines using [VirtualBox](https://www.virtualbox.org)
- A full installation on two **real** machines

## Installation using virtual machines

Please carry out the following steps:

1.  Install [VirtualBox](https://www.virtualbox.org).
2.  Install [Vagrant](https://www.vagrantup.com).
3.  Open a terminal window and carry out the following commands in the folder you want to install PPTAM:

    1.  `git clone https://github.com/pptam/pptam-tool.git`
    2.  `cd ./pptam-tool/installation`
    3.  `vagrant up`. You can see the video of this step [here](./attachments/setup_machines.mp4).
    4.  Once installation is finished, you can use the following commands **within the installation folder**:

        - `vagrant ssh driver` to ssh into the driver;
        - `vagrant ssh testbed` to ssh into the testbed;
        - `vagrant halt` to turn both machines off;
        - `vagrant up` to turn both machines on; and
        - `vagrant destroy` to delete the machines.

    5.  Continue, carrying out the following commands:

        - `vagrant ssh driver`
        - `cd /vagrant/scripts/`
        - `./get_pptam_development.sh` You can see the video of this step [here](./attachments/install_pptam.mp4).

## Full installation

To install PPTAM on two real machines, please carry out the following steps:

1. Setup two machines (which we call "driver" and "testbed") so that they can reach each other on a network. You can check the file [Vagrantfile](Vagrantfile) to see the minimal memory requirements for both machines and the ports we use to access the various tools.
2. Install Ubuntu 18.04.4 LTS on both machines.
3. The commands to install PPTAM on both machines can be found in [scripts/install_both.sh](scripts/install_both.sh), [scripts/install_driver.sh](scripts/install_driver.sh), and [scripts/install_testbed.sh](scripts/install_testbed.sh), but have to be adapted to your environment:

   - change the user "vagrant" to the user that will carry out the tests;
   - adapt the machine addresses, names, and user names to the ones you are using;
   - when creating a Docker swarm, `install_driver.sh` saves the join token in `/vagrant/.join-token-worker` so that `install_testbed.sh` can pick it up from there. When installing Docker swarm on two real machines, you can skip saving the token and execute the join instruction Docker displays when creating the swarm within the driver;
   - keep in mind that the /vagrant folder within the Vagrant installation scripts corresponds to the `installation` folder of the PPTAM repository. Whenever files are copied from `/vagrant` in the script, you need to copy them from the `installation` folder (e.g., the Jupyter Notebook configuration file)
