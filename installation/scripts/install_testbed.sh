
#!/bin/bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "  _____         _   _              _ ";
echo " |_   _|__  ___| |_| |__   ___  __| |";
echo "   | |/ _ \\/ __| __| '_ \\ / _ \\/ _\` |";
echo "   | |  __/\\__ \\ |_| |_) |  __/ (_| |";
echo "   |_|\\___||___/\\__|_.__/ \\___|\\__,_|";
echo "                                     ";

docker swarm join --advertise-addr $1 --listen-addr $1 --token $(cat /vagrant/.join-token-worker) $2
rm /vagrant/.join-token-worker

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl enable --now docker
sudo usermod -aG docker vagrant

sudo mkdir -p /etc/systemd/system/docker.service.d
cat <<EOF | sudo tee /etc/systemd/system/docker.service.d/override.conf >/dev/null
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd
EOF

sudo systemctl daemon-reexec
sudo systemctl restart docker
