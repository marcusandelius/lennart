#!/usr/bin/env bash
# Tillfällig testapp: visar att deploy-kedjan fungerar (push → runner → systemd).
# Ersätts av den riktiga Pi-appen när koden flyttats in.
set -euo pipefail

echo "Lennart startar på $(hostname)"
if [ -n "${LENNART_SERVER_URL:-}" ]; then
  echo "Server-adress är satt i .env"
else
  echo "Server-adress saknas i .env (ok under test)"
fi

while true; do
  echo "Lennart lever $(date '+%Y-%m-%d %H:%M:%S')"
  sleep 60
done
