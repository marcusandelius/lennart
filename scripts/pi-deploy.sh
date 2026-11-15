#!/usr/bin/env bash
# Körs av GitHub-runnern på Pi:n efter varje push till main.
#
# Vad skriptet gör, och varför:
# 1. Kopierar Pi-koden från runnerns arbetsmapp till en egen installationsmapp.
#    Runnern rensar sin arbetsmapp mellan jobb, så den körande appen ska inte bo där.
# 2. Installerar Python-beroenden i en virtuell miljö (om requirements.txt finns).
#    --system-site-packages gör att paket som bara finns via apt (t.ex. picamera2)
#    syns även i den virtuella miljön.
# 3. Installerar systemd-tjänsten som *användartjänst* och startar om den.
#    En användartjänst kräver inte sudo, så runnern behöver inga root-rättigheter.
#
# Hemligheter läses av tjänsten från ~/.config/lennart/.env, som aldrig rörs här.

set -euo pipefail

REPO_DIR="${GITHUB_WORKSPACE:-$(pwd)}"
SRC_DIR="${REPO_DIR}/pi"                     # Pi-koden i repot [osäkert: mappnamn bekräftas när koden flyttats in]
APP_DIR="${HOME}/lennart-app"                # där appen körs
UNIT_SRC="${REPO_DIR}/deploy/pi/lennart.service"
UNIT_DIR="${HOME}/.config/systemd/user"
ENV_FILE="${HOME}/.config/lennart/.env"

# systemctl --user behöver veta var användarens systemd-instans finns,
# eftersom runnern själv körs som systemtjänst.
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"

if [ ! -d "${SRC_DIR}" ]; then
  echo "::notice::Ingen Pi-kod i repot ännu (${SRC_DIR} saknas). Inget att installera."
  exit 0
fi

if [ ! -f "${ENV_FILE}" ]; then
  echo "::error::${ENV_FILE} saknas på Pi:n. Skapa den enligt docs/SETUP-PI.md."
  exit 1
fi

# Paketen installeras en gång för hand med apt (docs/SETUP-PI.md, steg 4).
# Kontrollera dem här, så att ett tydligt fel syns i GitHub i stället för en krasch.
if ! /usr/bin/python3 -c "import picamera2, spidev, lgpio, PIL, numpy" 2>/dev/null; then
  echo "::error::Python-paket saknas på Pi:n. Kör: sudo apt install -y python3-picamera2 python3-spidev python3-gpiozero python3-lgpio python3-pil python3-numpy --no-install-recommends"
  exit 1
fi

echo "→ Kopierar kod till ${APP_DIR}"
mkdir -p "${APP_DIR}"
rsync -a --delete --exclude '.venv/' "${SRC_DIR}/" "${APP_DIR}/"
# Vilken commit som körs, så att statussidan på lennart.cam kan visa det.
echo "${GITHUB_SHA:-okänd}" > "${APP_DIR}/VERSION"

if [ -f "${APP_DIR}/requirements.txt" ]; then
  echo "→ Installerar Python-beroenden"
  if [ ! -d "${APP_DIR}/.venv" ]; then
    python3 -m venv --system-site-packages "${APP_DIR}/.venv"
  fi
  "${APP_DIR}/.venv/bin/pip" install --quiet --upgrade pip
  "${APP_DIR}/.venv/bin/pip" install --quiet -r "${APP_DIR}/requirements.txt"
fi

echo "→ Installerar och startar om systemd-tjänsten"
mkdir -p "${UNIT_DIR}"
install -m 0644 "${UNIT_SRC}" "${UNIT_DIR}/lennart.service"
systemctl --user daemon-reload
systemctl --user enable lennart.service >/dev/null
systemctl --user restart lennart.service

# Ge tjänsten några sekunder och kontrollera att den lever.
sleep 5
if systemctl --user is-active --quiet lennart.service; then
  echo "✓ lennart.service är igång"
else
  echo "::error::lennart.service startade inte. Senaste loggraderna:"
  journalctl --user -u lennart.service -n 30 --no-pager || true
  exit 1
fi
