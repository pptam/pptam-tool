# Full installation

To install PPTAM on two real machines, please carry out the following steps:

1. Setup two machines (which we call "driver" and "testbed") so that they can reach each other on a network. You can check the file [Vagrantfile](Vagrantfile) to see the minimal memory requirements for both machines and the ports we use to access the various tools.
2. Install Ubuntu 18.04.4 LTS on both machines.
3. The commands to install PPTAM on both machines can be found in [scripts/install_both.sh](scripts/install_both.sh), [scripts/install_driver.sh](scripts/install_driver.sh), and [scripts/install_testbed.sh](scripts/install_testbed.sh), but have to be adapted to your environment:

   - change the user "vagrant" to the user that will carry out the tests;
   - adapt the machine addresses, names, and user names to the ones you are using;
   - when creating a Docker swarm, `install_driver.sh` saves the join token in `/vagrant/.join-token-worker` so that `install_testbed.sh` can pick it up from there. When installing Docker swarm on two real machines, you can skip saving the token and execute the join instruction Docker displays when creating the swarm within the driver;
   - keep in mind that the /vagrant folder within the Vagrant installation scripts corresponds to the `installation` folder of the PPTAM repository. Whenever files are copied from `/vagrant` in the script, you need to copy them from the `installation` folder (e.g., the Jupyter Notebook configuration file)
