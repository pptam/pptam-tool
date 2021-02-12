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
        - `./get_pptam.sh` (if you get "Permission denied", execute `chmod uog+x get_pptam.sh`)

    6.  If you want, you can do a test run:

        - `cd ~/pptam-tool/execute`
        - `./execute_test.py --design=../design_jsonserver_vagrant`

        You should now see the following output:

        Executing test case 202102120926-json-test1.
        Creating network 202102120926-json-test1_default
        Creating service 202102120926-json-test1_server
        Waiting for 10 seconds to allow the application to deploy.
        Collecting Docker stats #1 in background.

        Running the load test for 202102120926-json-test1, with 1000 users, running for 60 seconds.
        Collecting Docker stats of 202102120926-json-test1_server.1.y1er45elfl12tzjlkerzl4v42.
        Collecting Docker stats #2 in background.
        Collecting Docker stats of 202102120926-json-test1_server.1.y1er45elfl12tzjlkerzl4v42.
        Collecting Docker stats #3 in background.
        Collecting Docker stats of 202102120926-json-test1_server.1.y1er45elfl12tzjlkerzl4v42.
        Collecting Docker stats #4 in background.
        Collecting Docker stats of 202102120926-json-test1_server.1.y1er45elfl12tzjlkerzl4v42.
        Collecting Docker stats #5 in background.
        Collecting Docker stats of 202102120926-json-test1_server.1.y1er45elfl12tzjlkerzl4v42.
        Collecting Docker stats #6 in background.
        Collecting Docker stats of 202102120926-json-test1_server.1.y1er45elfl12tzjlkerzl4v42.

        Killing Docker stats thread.
        Stopping Docker stats in background.

        Removing service 202102120926-json-test1_server
        Removing network 202102120926-json-test1_default
        Waiting for 5 seconds to allow the application to undeploy.
        Test 202102120926-json-test1 completed. Test results can be found in /home/vagrant/pptam-tool/execute/executed/202102120926-json-test1.
        Done.
