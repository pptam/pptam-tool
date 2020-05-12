#!/bin/bash 

echo INSTALLING WORKER
echo ==================================================================

set -e

docker swarm join --advertise-addr $1 --listen-addr $1 --token `cat /vagrant/.join-token-worker` $2
rm /vagrant/.join-token-worker
