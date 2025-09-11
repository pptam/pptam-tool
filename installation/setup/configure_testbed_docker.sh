#!/usr/bin/env bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  exec sudo "$0" "$@"
fi

mkdir -p /etc/docker

if [ -f /etc/docker/daemon.json ]; then
  if grep -q 'default-pids-limit' /etc/docker/daemon.json; then
    sed -i 's/"default-pids-limit"[[:space:]]*:[[:space:]]*[0-9]\+/"default-pids-limit": 1/' /etc/docker/daemon.json
  else
    sed -i '1s/^/{\n  "default-pids-limit": 1,\n/' /etc/docker/daemon.json
  fi
else
  echo '{"default-pids-limit": 1}' > /etc/docker/daemon.json
fi

systemctl daemon-reload
systemctl restart docker

echo "Default PID limit set to 1 for all containers."