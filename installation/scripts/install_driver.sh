#!/bin/bash 
set -e

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=Driver%20setup
echo "  ____       _                           _               ";
echo " |  _ \ _ __(_)_   _____ _ __   ___  ___| |_ _   _ _ __  ";
echo " | | | | '__| \ \ / / _ \ '__| / __|/ _ \ __| | | | '_ \ ";
echo " | |_| | |  | |\ V /  __/ |    \__ \  __/ |_| |_| | |_) |";
echo " |____/|_|  |_| \_/ \___|_|    |___/\___|\__|\__,_| .__/ ";
echo "                                                  |_|    ";

# Docker swarm installation and writing join token into file
docker swarm init --advertise-addr $1 --listen-addr $1
docker swarm join-token -q worker > /vagrant/.join-token-worker

# Python installation
apt install -y python3.9 python3.9-dev python3-pip 
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
sudo update-alternatives --set python /usr/bin/python3.9

sudo update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.9 1
sudo update-alternatives --set pip /usr/local/bin/pip3.9

sudo pip install -r /home/vagrant/requirements.txt

# Update to the last version of Git and configure it
sudo add-apt-repository ppa:git-core/ppa -y
sudo apt-get update
sudo apt-get install git -y

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Setup PPTAM
cd /home/vagrant/
git clone --depth 1 https://github.com/pptam/pptam-tool.git
