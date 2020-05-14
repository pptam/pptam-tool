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

1. Install [VirtualBox](https://www.virtualbox.org).
2. Install [Vagrant](https://www.vagrantup.com).
3. Open a terminal window and carry out the following commands:

   1. Download this project using `git clone https://github.com/pptam/pptam-tool.git` within your preferred folder.
   2. Within the `installation` subfolder of the cloned project, execute `vagrant up`.

You can see the video of this step [here](documentation/1-setup machines.mp4).
