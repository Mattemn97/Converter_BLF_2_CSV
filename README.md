# Converter_BLF_2_CSV
Questo programma converte i file di log della rete CAN in formato .blf in file .csv, utilizzabili facilmente da strumenti come PlotJuggler.
Utilizza uno o più file .dbc per interpretare i messaggi CAN e fornisce un'interfaccia grafica per una facile gestione.

## Caratteristiche
- **Conversione da BLF a CSV**: Converte i file di log .blf in file .csv.
- **Supporto per file DBC multipli**: Utilizza file .dbc per interpretare i messaggi CAN.
- **Interfaccia grafica**: Consente di selezionare facilmente i file .blf e le cartelle contenenti i file .dbc.
- **Monitoraggio avanzamento**: Una barra di caricamento mostra lo stato del processo, con dettagli su cosa il programma sta facendo in tempo reale.
- **Ottimizzazione delle dimensioni del CSV**: Aggiunge solo le righe con valori aggiornati, riducendo le dimensioni del file CSV.
- **Eseguibile pronto all'uso**: Disponibile una versione .exe per chi desidera eseguire il programma senza configurazioni aggiuntive.

## Requisiti
- Python 3.x
- Librerie Python: can, csv, dbc, python-can, cantools, tqdm, tkinter

## Installazione
1. Clona la repository:
   ```bash
   git clone https://github.com/tuo-username/Converter_BLF_2_CSV.git
   ```
   ```bash
   cd Converter_BLF_2_CSV
   ```

3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

## Utilizzo
### Avvio versione Python
1) Esegui il programma: Avvia l'interfaccia grafica con il seguente comando:

```bash
python main.py
```

2) Seleziona il file di log: Usa il pulsante "Seleziona File Log" per scegliere un file .blf.
3) Seleziona la cartella dei file DBC: Usa il pulsante "Seleziona Cartella DBC" per indicare la cartella contenente i file .dbc.
4) Avvia la conversione: Clicca su "Avvia Conversione" per avviare il processo. Una barra di avanzamento mostrerà lo stato della conversione.

### Avvio versione eseguibile
Per chi non desidera configurare Python e le librerie, è possibile scaricare l'eseguibile .exe dalla sezione Release della repository.

1) Vai alla sezione Release del repository.
2) Scarica il file main.exe.
3) Esegui il file .exe e utilizza l'interfaccia grafica per convertire i file .blf in .csv.

## Contributi
I contributi sono benvenuti! Sentiti libero di aprire issue e pull request.

## Licenza
Questo progetto è distribuito sotto la licenza GPL-3.0. Vedi il file LICENSE per maggiori dettagli.
