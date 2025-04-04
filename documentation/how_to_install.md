# Installation

This documentation needs to be updated...

PPTAM is supposed to be installed on two Linux machines:

- The "driver": a machine to **control** the experiment.
- The "testbed": a machine to **execute** the experiment.

The installation requires to setup both machines so that they can reach each other on a network and install [Docker](https://www.docker.com) on both machines. Only on the driver, you have to install PPTAM to control and visualize the output of experiments.

To make it easier to try out and play with PPTAM, we foresee two types of installation:

- See [here](./how_to_install_on_virtualbox.md) for the installation using two **virtual** machines using [VirtualBox](https://www.virtualbox.org)
- See [here](./how_to_install_full.md) for the full installation on two **real** machines

Notes to update:
- docker can be run without sudo (add to the docker group and sudo chown $USER /var/run/docker.sock)
- sudo snap restart docker

- Configuration needed so that PPTAM can restart docker without password
sudo visudo
power ALL=(ALL) NOPASSWD: /usr/bin/snap restart docker 