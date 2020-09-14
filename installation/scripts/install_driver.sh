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

# Java installation
apt install -y openjdk-8-jdk ant python3.8 python3.8-dev
echo JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/" >> /etc/environment

# Making sure python works
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
sudo update-alternatives --set python /usr/bin/python3.8

# Installion of Jupyter Notebook
cd /home/vagrant
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -nv -O /tmp/miniconda.sh
bash /tmp/miniconda.sh -b -p /home/vagrant/miniconda

echo export PATH=/home/vagrant/miniconda/bin:$PATH >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc

eval "$(/home/vagrant/miniconda/bin/conda shell.bash hook)"
conda init
conda install -c r r-essentials -y
conda install -c conda-forge notebook -y
conda install -c anaconda python=3.8 pip -y
pip install requests locust psutil influxdb-client

cp -r /vagrant/configuration/jupyter /home/vagrant/.jupyter

# Update to the last version of Git
sudo add-apt-repository ppa:git-core/ppa -y
sudo apt-get update
sudo apt-get install git -y
