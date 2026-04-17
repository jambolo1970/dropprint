# DropPrint

DropPrint è una piccola applicazione desktop per Linux che permette di trascinare file su una finestra e inviarli subito alla stampante selezionata tramite CUPS.

## Funzioni principali

- drag and drop multiplo dei file
- selezione stampante attiva
- monitoraggio stato dei job CUPS
- colori rapidi:
  - rosso = in coda / in attesa
  - arancione = in stampa
  - verde = completato
  - rosso scuro = annullato o errore
- rimozione automatica dei job dalla lista dopo 60 secondi
- icona nel system tray
- click sul tray per aprire o nascondere la finestra
- chiusura finestra senza terminare il programma

## Requisiti

- Linux con CUPS attivo
- Python 3.10+
- PyQt6
- pycups

## Avvio rapido

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
dropprint
```

## Installazione su openSUSE Leap 15.5

```bash
chmod +x packaging/install_opensuse.sh
./packaging/install_opensuse.sh
```
In caso di problemi con i repository sostituire nel file `ìnstall_opensuse.sh` nella riga 12 dovrebbe esserci scritto `sudo zypper --non-interactive refresh` sostituire con :
```bash
if command -v zypper >/dev/null 2>&1; then
  echo "==> Refresh repository (ignoro eventuali errori)"
  sudo zypper --non-interactive --gpg-auto-import-keys refresh || true

  echo "==> Installazione dipendenze base"
  if ! sudo zypper --non-interactive install --no-refresh \
      python311 python311-pip python311-setuptools python311-wheel \
      python311-devel gcc cups cups-client cups-devel; then
    echo "==> Fallback a python3"
    sudo zypper --non-interactive install --no-refresh \
      python3 python3-pip python3-setuptools python3-wheel \
      python3-devel gcc cups cups-client cups-devel || true
  fi
else
  echo "zypper non trovato. Questo script è pensato per openSUSE."
  exit 1
fi
```
in questo caso si fermerà solo se manca qualche dipendenza che serve all'utility


Lo script:
- installa le dipendenze di sistema
- installa DropPrint in `~/.local`
- copia il file `.desktop`
- installa l'icona
- crea un comando `dropprint`

## Repository

```text
dropprint-github/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── src/dropprint/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py
│   └── assets/
│       ├── dropprint.png
│       └── dropprint.svg
└── packaging/
    ├── install_opensuse.sh
    └── dropprint.desktop
```

## Note tecniche

Il bug originale nasceva dal fatto che in CUPS/IPP lo stato del job è esposto come `job-state`, non come `state`. Inoltre i job completati possono sparire dalla lista generale, quindi è più robusto interrogare gli attributi del singolo job con `getJobAttributes(job_id)`. Qt prevede il tray tramite `QSystemTrayIcon`, con verifica preventiva della disponibilità del vassoio di sistema.

## Licenza

MIT
