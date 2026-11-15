#!/usr/bin/env bash
# Startar Pi-appen. Körs av systemd-tjänsten lennart.service.
# Systemets Python används, eftersom kamerabiblioteket picamera2 installeras med apt.
set -euo pipefail
cd "$(dirname "$0")"
exec /usr/bin/python3 -u main.py
