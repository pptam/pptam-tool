#!/usr/bin/env bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  exec sudo "$0" "$@"
fi

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y curl tar

VERSION=$(curl -s https://api.github.com/repos/hubblo-org/scaphandre/releases/latest | grep tag_name | cut -d '"' -f4)

mkdir -p /tmp/scaphandre
cd /tmp/scaphandre

curl -sL https://github.com/hubblo-org/scaphandre/releases/download/${VERSION}/scaphandre-${VERSION}-x86_64-unknown-linux-gnu.tar.gz -o scaphandre.tar.gz
tar -xzf scaphandre.tar.gz

install scaphandre /usr/local/bin/scaphandre

cat <<EOF >/etc/systemd/system/scaphandre.service
[Unit]
Description=Scaphandre power monitoring agent
After=network.target

[Service]
ExecStart=/usr/local/bin/scaphandre json
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now scaphandre

echo "Scaphandre is installed and running."