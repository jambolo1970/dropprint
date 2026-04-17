#!/usr/bin/env bash
set -euo pipefail

APP_NAME="dropprint"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
LOCAL_APPS="${HOME}/.local/share/applications"
LOCAL_ICONS="${HOME}/.local/share/icons/hicolor/256x256/apps"

echo "==> Installazione dipendenze di sistema per openSUSE Leap 15.5"

if command -v zypper >/dev/null 2>&1; then
  sudo zypper --non-interactive refresh
  sudo zypper --non-interactive install \
    python311 python311-pip python311-setuptools python311-wheel \
    python311-devel gcc cups cups-client cups-devel
else
  echo "zypper non trovato. Questo script è pensato per openSUSE."
  exit 1
fi

echo "==> Installazione dipendenze Python utente"
"${PYTHON_BIN}" -m pip install --user --upgrade pip
"${PYTHON_BIN}" -m pip install --user PyQt6 pycups
"${PYTHON_BIN}" -m pip install --user "${PROJECT_ROOT}"

echo "==> Installazione launcher desktop"
mkdir -p "${LOCAL_APPS}" "${LOCAL_ICONS}"
cp "${PROJECT_ROOT}/packaging/dropprint.desktop" "${LOCAL_APPS}/dropprint.desktop"
cp "${PROJECT_ROOT}/src/dropprint/assets/dropprint.png" "${LOCAL_ICONS}/dropprint.png"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "${LOCAL_APPS}" || true
fi

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache "${HOME}/.local/share/icons/hicolor" || true
fi

echo
echo "Installazione completata."
echo "Avvio con: dropprint"
