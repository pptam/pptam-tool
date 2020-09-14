# Installation using virtual machines

Please carry out the following steps:

1.  Install [VirtualBox](https://www.virtualbox.org).
2.  Install [Vagrant](https://www.vagrantup.com).
3.  Open a terminal window and carry out the following commands in the folder you want to install PPTAM:

    1.  `git clone https://github.com/pptam/pptam-tool.git`
    2.  `cd ./pptam-tool/installation`
    3.  `vagrant up`
    4.  Once installation is finished, these are the available commands **within the installation folder**:

        - `vagrant ssh driver` to ssh into the driver;
        - `vagrant ssh testbed` to ssh into the testbed;
        - `vagrant halt` to turn both machines off;
        - `vagrant up` to turn both machines on; and
        - `vagrant destroy` to delete the machines.
        - `vagrant reload` to reboot the machines.

    5.  Now, execute the following commands:

        - `vagrant ssh driver`
        - `cd /vagrant/scripts/`
        - `./get_pptam.sh`
