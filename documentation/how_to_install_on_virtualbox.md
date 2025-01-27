# Installation using virtual machines

Please carry out the following steps *on your computer*:

1.  Install [VirtualBox](https://www.virtualbox.org).
2.  Install [Vagrant](https://www.vagrantup.com).
3.  Install [Git](https://git-scm.com/downloads).
4.  Open a terminal window, navigate to a folder where you want to *download* PPTAM and carry out the following commands:

    1.  `git clone https://github.com/pptam/pptam-tool.git`
    2.  `cd ./pptam-tool/installation`
    3.  `vagrant up` (This step might take some time since images have to be dowloaded and two virtual machines will be configured with the necessary software; in our case it took 1 hour)
    
5.  Once installation is finished, these are the available commands **within the installation folder**:

    - `vagrant ssh driver` to ssh into the driver;
    - `vagrant ssh testbed` to ssh into the testbed;
    - `vagrant halt` to turn both machines off;
    - `vagrant up` to turn both machines on; 
    - `vagrant destroy` to delete the machines; and
    - `vagrant reload` to reboot the machines.

6.  Now, execute the following command *on your computer*:

    - `vagrant ssh driver`

    After this instruction you should have logged into the *driver* machine. There, please execute the following commands:

7.  If you want, you can do a test run now:

    - `cd ~/pptam-tool/toolchain`
    - `./execute.py --design=../design_jsonserver_vagrant`

    You should now see a similar output:

    ```
    Executing test case 202102120945-json-test1.
    Creating network 202102120945-json-test1_default
    Creating service 202102120945-json-test1_server
    Waiting for 10 seconds to allow the application to deploy.
    Running the load test for 202102120945-json-test1, with 1000 users, running for 60 seconds.
    Removing service 202102120945-json-test1_server
    Removing network 202102120945-json-test1_default
    Waiting for 5 seconds to allow the application to undeploy.
    Test 202102120945-json-test1 completed. Test results can be found in /home/vagrant/pptam-tool/toolchain/executed/undefined/00000000/202102120945-json-test1.
    Done.
    ```

    If you now check the `~/pptam-tool/toolchain/executed` folder, you will find a folder of the just executed experiment, and in this folder the results of the experiment. You can find out more about what the various output files mean [here](./how_to_use.md).
    If the --projectname if defined you will find everything in a folder like this: `~/pptam-tool/toolchain/executed/projectname/commit`

    This should be the output of `locustfile.out`:
    ```
    Name         # reqs   # fails  |  Avg  Min  Max  Median  |   req/s failures/s
    -------------------------------------------------------------------------------
    GET /cars       146  0(0.00%)  |   15    5  105       9  |    2.43    0.00
    GET /cars/1     173  0(0.00%)  |   18    3  226       9  |    2.88    0.00
    GET /cars/2     162  0(0.00%)  |   17    4  134       8  |    2.70    0.00
    GET /cars/3     170  0(0.00%)  |   16    3  127       8  |    2.83    0.00
    GET /cars/4     164  0(0.00%)  |   15    3  151       7  |    2.73    0.00
    GET /cars/5     177  0(0.00%)  |   17    3  105       8  |    2.95    0.00
    GET /cars/6     153  0(0.00%)  |   16    3  132       8  |    2.55    0.00
    GET /cars/7     170  0(0.00%)  |   17    3  118       8  |    2.83    0.00
    GET /cars/8     179  0(0.00%)  |   15    4  135       8  |    2.98    0.00
    GET /cars/9     167  0(0.00%)  |   18    3  113       8  |    2.78    0.00
    -------------------------------------------------------------------------------
    Aggregated     1661  0(0.00%)  |   16    3  226       8  |   27.68    0.00

    Response time percentiles (approximated)
    Type   Name         50%  66%  75%  80%  90%  95%  98%  99%  99.9% 99.99%  100% # reqs
    ------|------------|----|----|----|----|----|----|----|----|------|------|-----|------|
    GET    /cars          9   11   14   18   29   59   81   87    110    110   110    146
    GET    /cars/1        9   13   20   25   43   58   85  130    230    230   230    173
    GET    /cars/2        8   11   17   24   49   61  110  120    130    130   130    162
    GET    /cars/3        8   12   18   26   41   48   69   95    130    130   130    170
    GET    /cars/4        7    9   14   19   40   50   77  100    150    150   150    164
    GET    /cars/5        8   13   21   27   45   54   78   85    110    110   110    177
    GET    /cars/6        8   11   18   23   44   50   79  120    130    130   130    153
    GET    /cars/7        8   11   15   25   46   60   81   99    120    120   120    170
    GET    /cars/8        8   12   15   22   41   53   74  130    140    140   140    179
    GET    /cars/9        8   14   24   32   44   55   93  110    110    110   110    167
    ------|------------|----|----|----|----|----|----|----|----|------|------|-----|------|
    None   Aggregated     8   12   17   24   44   55   79  110    150    230   230   1661
    ```./sto