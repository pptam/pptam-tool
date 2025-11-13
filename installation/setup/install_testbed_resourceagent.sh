#!/usr/bin/env bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  exec sudo "$0" "$@"
fi

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y python3 python3-venv python3-pip python3-dev build-essential docker.io

rm -rf /opt/resourceagent
mkdir -p /opt/resourceagent
cp -r ./toolchain/tools/resource_agent/. /opt/resourceagent/

python3 -m venv /opt/resourceagent/.venv
/opt/resourceagent/.venv/bin/pip install --upgrade pip
/opt/resourceagent/.venv/bin/pip install flask docker
chown -R root:root /opt/resourceagent

cat <<'EOF' >/etc/systemd/system/resourceagent.service
[Unit]
Description=Resourceagentapp
After=docker.service
Requires=docker.service

[Service]
Type=simple
WorkingDirectory=/opt/resourceagent
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/resourceagent/.venv/bin/python app.py
Restart=on-failure
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now resourceagent
systemctl status --no-pager resourceagent
