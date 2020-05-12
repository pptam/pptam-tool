#!/bin/bash 

echo INSTALLING DOCKER
echo ==================================================================

apt-get update
apt-get upgrade -y
curl -sSL https://get.docker.com/ | sh
usermod -aG docker vagrant

echo 192.168.50.100 driver >> /etc/hosts
echo 192.168.50.101 testbed >> /etc/hosts