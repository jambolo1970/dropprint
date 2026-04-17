#!/bin/bash

#
#    Nome programma: Crea Lanciatore
#    Autore: Gianluca Bolognesi
#    Versione: Aprile 2026
#    Descrizione: programma bash per creare un lanciatore ed installarlo nel menu.
#

# --- DEFINIZIONE COLORI ---
ROSSO='\033[0;31m'
VERDE='\033[0;32m'
NC='\033[0m' # No Color

# 1. Ottiene il percorso assoluto
DIR_ATTUALE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# 2. Crea il file .desktop
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

# 4. Lo copia nella cartella delle applicazioni dell'utente
cp DropPrint.desktop ~/.local/share/applications/

# --- CONTROLLO FINALE ---
# Verifichiamo se il file esiste nella destinazione finale
if [ -f ~/.local/share/applications/DropPrint.desktop ]; then
    echo -e "${VERDE}[OK]${NC} Installazione completata! DropPrint è ora nel tuo menu applicazioni."
else
    echo -e "${ROSSO}[ERRORE]${NC} Qualcosa è andato storto nell'installazione!"
    exit 1
fi
