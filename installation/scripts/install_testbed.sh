#!/bin/bash 
set -e

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=Testbed%20setup
echo "  _____         _   _              _            _               ";
echo " |_   _|__  ___| |_| |__   ___  __| |  ___  ___| |_ _   _ _ __  ";
echo "   | |/ _ \/ __| __| '_ \ / _ \/ _\` | / __|/ _ \ __| | | | '_ \ ";
echo "   | |  __/\__ \ |_| |_) |  __/ (_| | \__ \  __/ |_| |_| | |_) |";
echo "   |_|\___||___/\__|_.__/ \___|\__,_| |___/\___|\__|\__,_| .__/ ";
echo "                                                         |_|    ";

# Docker swarm installation: picking up the join token and adding testbad to the swarm
docker swarm join --advertise-addr $1 --listen-addr $1 --token `cat /vagrant/.join-token-worker` $2
rm /vagrant/.join-token-worker

# https://gist.github.com/styblope/dc55e0ad2a9848f2cc3307d4819d819f
echo {"hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]} >> /etc/docker/daemon.json
mkdir /etc/systemd/system/docker.service.d
echo [Service] >> /etc/systemd/system/docker.service.d/override.conf
echo ExecStart= >> /etc/systemd/system/docker.service.d/override.conf
echo ExecStart=/usr/bin/dockerd >> /etc/systemd/system/docker.service.d/override.conf
systemctl daemon-reload
systemctl restart docker.service