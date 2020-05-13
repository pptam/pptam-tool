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
apt-get update
apt-get upgrade -y
curl -sSL https://get.docker.com/ | sh
usermod -aG docker vagrant

# Adding both machines to the hosts file so that they can be found by name 
echo 192.168.50.100 driver >> /etc/hosts
echo 192.168.50.101 testbed >> /etc/hosts