echo INSTALLING DRIVER

set -e

docker swarm init --advertise-addr $1 --listen-addr $1
docker swarm join-token -q worker > /vagrant/.join-token-worker

apt install -y openjdk-8-jdk ant
echo JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/" >> /etc/environment