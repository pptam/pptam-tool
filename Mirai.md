# Adding Mirai as a possible attack during testing

To use Mirai to attack a particular end point during testing, we modified benchflow.sh inside the test executor so that the attack is launched after 180 seconds of running a test. Moreover, we use a modified version of Mirai that only attacks without infecting the system.

**Only** on the **driver** machine perform the following operations:

1. Modify benchflow.sh and uncomment the following lines:
   - #echo "RUN MIRAI!!!!"
   - #../miraibot/miraibot -t 1200 -a HTTP -i 10.7.20.69 24 256 &
2. Download and compile the Mirai bot from https://github.com/queupe/Mirai-Source-Code and add the miraibot folder to your home folder.

