#!/usr/bin/env bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  exec sudo "$0" "$@"
fi

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y golang-go git build-essential

if [ ! -d /opt/cadvisor ]; then
  git clone https://github.com/google/cadvisor.git /opt/cadvisor
fi

cd /opt/cadvisor
make build

cp /opt/cadvisor/_output/cadvisor /usr/local/bin/cadvisor

cat <<EOF >/etc/systemd/system/cadvisor.service
[Unit]
Description=cAdvisor
After=network.target

[Service]
ExecStart=/usr/local/bin/cadvisor
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now cadvisor

echo "cAdvisor is running on http://localhost:8080"