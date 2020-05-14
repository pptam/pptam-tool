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
3.  Open a terminal window and carry out the following commands:

    1.  `git clone https://github.com/pptam/pptam-tool.git`
    2.  `cd ./pptam-tool/installation`
    3.  `vagrant up`. You can see the video of this step [here](./documentation/setup_machines.mp4).
    4.  Once installation is finished, you can use the following commands **within the installation folder**:

        - `vagrant ssh driver` to ssh into the driver;
        - `vagrant ssh testbed` to ssh into the testbed;
        - `vagrant halt` to turn both machines off;
        - `vagrant up` to turn both machines on; and
        - `vagrant destroy` to delete the machines.

    5.  Continue, carrying out the following commands:

        - `vagrant ssh driver`
        - `cd /vagrant/scripts/`
        - `./get_pptam_development.sh` You can see the video of this step [here](./documentation/install_pptam.mp4).
