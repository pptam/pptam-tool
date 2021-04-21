#!/bin/bash 
set -e

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=Generic%20setup
echo "   ____                      _                 _               ";
echo "  / ___| ___ _ __   ___ _ __(_) ___   ___  ___| |_ _   _ _ __  ";
echo " | |  _ / _ \ '_ \ / _ \ '__| |/ __| / __|/ _ \ __| | | | '_ \ ";
echo " | |_| |  __/ | | |  __/ |  | | (__  \__ \  __/ |_| |_| | |_) |";
echo "  \____|\___|_| |_|\___|_|  |_|\___| |___/\___|\__|\__,_| .__/ ";
echo "                                                        |_|    ";

# Installing docker 
sudo apt-get update
sudo apt-get upgrade -y
curl -sSL https://get.docker.com/ | sh

# Add the user that will carry out the tests to the docker group
usermod -aG docker vagrant

# Adding both machines to the hosts file so that they can be found by name 
sudo echo 192.168.50.100 driver >> /etc/hosts
sudo echo 192.168.50.101 testbed >> /etc/hosts

sudo echo * - nofile 100000 >> /etc/security/limits.conf



