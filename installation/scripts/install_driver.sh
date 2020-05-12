#!/bin/bash 

echo INSTALLING DRIVER
echo ==================================================================

set -e

docker swarm init --advertise-addr $1 --listen-addr $1
docker swarm join-token -q worker > /vagrant/.join-token-worker

apt install -y openjdk-8-jdk ant 
echo JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/" >> /etc/environment

# Fixes error "ModuleNotFoundError: No module named 'apt_pkg'"
# https://askubuntu.com/questions/1069087/modulenotfounderror-no-module-named-apt-pkg-error
# cd /usr/lib/python3/dist-packages
# sudo ln -s apt_pkg.cpython-35m-x86_64-linux-gnu.so apt_pkg.so

# sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
# sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
# sudo update-alternatives --set python /usr/bin/python3.7

# sudo apt-get install python-apt