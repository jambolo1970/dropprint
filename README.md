# DropPrint 🦎🖨️

DropPrint è una piccola applicazione desktop per Linux, principalmente **OpenSuse** (ma dovrebbe funzionare anche su altre distro Linux) che permette di trascinare file su una finestra e inviarli subito alla stampante selezionata, ci si appoggia al server di stampa CUPS, diventa molto utile se i file sono parecchi, ad esempio la stampa di estratti conto, copie di fatture xml trasformate in pdf, questo in un ambito ufficio, oppure in contesti dove si mandano in stampa molti file.
Tutto questo lo si fa tramite la funzione semplice del drag-and-drop, cioè selezionate e trascinate all'interno della finesta, prima però selezionate la stampante che volete utilizzare, perché una volta inseriti all'interno della finesta di DropPrint la stampa è immediata.
È perfetto per file immagine e PDF, gestite appunto da CUPS.

## ℹ️ Funzioni principali

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

Guarda il video dimostrativo su [YouTube]([https://www.youtube.com/watch?v=xhwxjXZ4zBk](https://youtu.be/xhwxjXZ4zBk).

[![Guarda il Video su YouTube di come OpenSuse comprime il file](https://img.youtube.com/vi/xhwxjXZ4zBk/0.jpg)]([https://www.youtube.com/watch?v=xhwxjXZ4zBk])


## ℹ️ Caratteristiche
- 🚀 **Batch Printing**: trascina decine di file e stampali tutti insieme.
- 📋 **Coda visibile**: monitora quali file sono stati inviati con successo.
- 🎛️ **Selezione stampante**: cambia al volo la stampante di destinazione.
- 🐧 **Ottimizzato per openSUSE**: integrazione perfetta con CUPS.
- 📄 **Tipi di file supportati**: CUPS gestisce nativamente PDF, immagini (JPG, PNG)
  - aggiunta compatibilità con formati :
  - ".odt", ".ods", ".odp" ---> LibreOffice / OpenOffice
  - ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx" --> MS Office (potrebbero non essere 100% impaginati correttamente, soprattutto DOCX complessi)
  - ".rtf", ".csv" 
- **File non supportati**: Se trascini un file non supportato non viene accettato, CUPS potrebbe non sapere come renderizzarlo a meno che non ci siano librerie che lo supportino

## ⚙️ Requisiti

- Linux con CUPS attivo
- Python 3.10+
- PyQt6
- pycups
- LibreOffice già installato
  - Serve se si vuole stampare direttamente file openDocument di LibreOffice
     
## 🖥️ Installazione su linux in generale
- Clicca sul tasto in alto a destra verde --> download ZIP
  - oppure: **Clona il repository:** e estrai lo zip.
  - apri un terminale ```git clone https://github.com/jambolo1970/dropprint.git```
  - ```cd dropprint```
- Vai nella cartella /home/UTENTE/Scaricati/ e scompatta dropprint-main.zip se usato il primo metodo
  - altrimenti col secondo metodo si chiamerà semplicemente dropprint 
- Entra nella cartella e apri il terminale, poi segui i passagi sotto

## 💻 Installazione su openSUSE/LinuxMint
Assicurati di avere le dipendenze di sistema:
```bash
sudo zypper install python3-pycups python3-qt6
```

## 🚀 Avvio rapido

Apri un terminale nella directory dove si trova il programma dropprint.py
```bash
cd ~/Scaricati/dropprint-main/
chmod +x dropprint.py
```
per lanciare il programma in modo diretto

```
python3 dorpprint.py
```
per avere un icona e niente terminali, apri il terminale
```bash
cd ~/Scaricati/dropprint-main/
chmod +x crea-lanciatore.sh
./crea-lanciatore.sh
```
a questo punto vi trovate l'icona nel menu all'interno di **Accessori** e una volta lanciato sarà presente nel vassoio di sistema in basso a destra come icona **DP**, cliccando sopra si aprirà la finestra ed all'interno potete trascinare i vostri file supportati.

## ♻️ Disinstallazione
Per rimuovere l'applicazione se è stato utilizzato crea-lanciatore.sh :
```bash
chmod +x rimuovi-lanciatore
./rimuovi-lanciatore.sh
```

## 👨‍🔧 Note tecniche
- se si effetuano modifiche al file dropprint.py contenuto nella cartella /Scaricati/dropprint-main/ le modifiche avverranno anche nel programma in modo diretto, in caso di aggiornamenti, conviene aggiornare il contenuto di solo quel file.
- Se avete segnalazioni o migliorie da far fare comunicatelo, per ora la struttura è molto semplice, di fatto prendi i file butti dentro e lui manda in stampa immediata

## Aggiornamenti
- 2026.04.19 : È stata aggiunta compatibilità anche per i file LibreOffice, vengono di fatto convertiti all'interno della cartella `/tmp `  conetnuta in dropprint in file pdf, non è  garantita piena compatibilità con i file MS Office, potrebbero esserci differenze d'impaginazione
- 2026.04.20 : È stato aggiornato il lanciatore, ora compatibile anche con LinuxMint e simili, in più ho aggiunto anche la possibilità di rimuovere l'installazione con rimuovi-lanciatore.sh.

  
## 📜 Licenza

MIT
