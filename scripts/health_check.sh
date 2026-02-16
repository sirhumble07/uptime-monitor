#!/usr/bin/env bash
set -euo pipefail

echo "=== Uptime Monitor Health Check ==="
echo "Timestamp: $(date -Is)"
echo

echo "[Containers]"
docker ps
echo

echo "[API health]"
curl -sS http://localhost/api/health || true
echo

echo "[Recent logs - worker]"
docker logs uptime-worker --tail 50 || true
echo

echo "[Recent logs - api]"
docker logs uptime-api --tail 50 || true
