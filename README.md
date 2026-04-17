# DropPrint 🦎🖨️

DropPrint è una piccola applicazione desktop per Linux, principalmente **OpenSuse** (ma dovrebbe funzionare anche su altre distro Linux) che permette di trascinare file su una finestra e inviarli subito alla stampante selezionata tramite CUPS, diventa molto utile se i file sono parecchi, ad esempio la stampa di estratti conto, copie di fatture xml trasformate in pdf.
Tutto questo lo si fa tramite la funzione semplice del drag-and-drop, cioè lo selezionate e trascinate all'interno della finesta, prima però selezionate la stampante che volete utilizzare.
È perfetto per file immagine e PDF, gestite da CUPS

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


## Caratteristiche
- 🚀 **Batch Printing**: trascina decine di file e stampali tutti insieme.
- 📋 **Coda visibile**: monitora quali file sono stati inviati con successo.
- 🎛️ **Selezione stampante**: cambia al volo la stampante di destinazione.
- 🐧 **Ottimizzato per openSUSE**: integrazione perfetta con CUPS.
- 📄 **Tipi di file supportati**: CUPS gestisce nativamente PDF, immagini (JPG, PNG)
- **File non supportati**: Se trascini un file .docx, CUPS potrebbe non sapere come renderizzarlo a meno che non ci siano librerie che lo supportino

## Requisiti

- Linux con CUPS attivo
- Python 3.10+
- PyQt6
- pycups

## Installazione su openSUSE
Assicurati di avere le dipendenze di sistema:
```bash
sudo zypper install python3-pycups python3-qt6
```

## Avvio rapido

Apri un terminale nella directory dove si trova il programma dropprint.py
```bash
cd ~/Scaricati/dropprint/
chmod +x dropprint.py
```
per lanciare il programma

```
python3 dorpprint.py
```

## Installazione su openSUSE Leap 15.5

```bash
chmod +x packaging/install_opensuse.sh
./packaging/install_opensuse.sh
```
``

## Note tecniche

Se avete segnalazioni o migliorie da far fare comunicatelo, per ora la struttura è molto semplice

## Licenza

MIT
