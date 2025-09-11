#!/bin/bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "  ____       _                ";
echo " |  _ \\ _ __(_)_   _____ _ __ ";
echo " | | | | '__| \\ \\ / / _ \\ '__|";
echo " | |_| | |  | |\\ V /  __/ |   ";
echo " |____/|_|  |_| \\_/ \\___|_|   ";
echo "                              ";

docker swarm init --advertise-addr $1 --listen-addr $1
docker swarm join-token -q worker > /vagrant/.join-token-worker

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-dev python3-pip git

# python3 -m pip install --upgrade pip
# pip install -r /home/vagrant/requirements.txt

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# cd /home/$USER/
# git clone --depth 1 https://github.com/pptam/pptam-tool.git
