
## `uptime-monitor/scripts/deploy.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${1:-$HOME/uptime-monitor}"

echo "Deploying in: $APP_DIR"
cd "$APP_DIR"

if [ ! -f .env ]; then
  echo "ERROR: .env not found. Create it from .env.example first."
  exit 1
fi

git pull
docker compose up -d --build
docker ps
