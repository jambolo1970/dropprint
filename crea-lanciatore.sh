#!/bin/bash

# 1. Ottiene il percorso assoluto della cartella dove si trova lo script
DIR_ATTUALE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# 2. Crea il file .desktop scrivendo i percorsi reali calcolati al momento
echo "[Desktop Entry]
Name=DropPrint
Comment=Stampa Tutto
Exec=python3 $DIR_ATTUALE/dropprint.py
Path=$DIR_ATTUALE
Icon=$DIR_ATTUALE/img/logo-dropprint.svg
Terminal=false
Type=Application
StartupNotify=true
Categories=Utility;" > DropPrint.desktop

# 3. Rende il file eseguibile
chmod +x DropPrint.desktop

# 4. Lo copia nella cartella delle applicazioni dell'utente così appare nel menu
cp DropPrint.desktop ~/.local/share/applications/

echo "Installazione completata! DropPrint è ora nel tuo menu applicazioni."
