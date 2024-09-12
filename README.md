# Converter_BLF/TRC_2_CSV
Questo programma converte i file di log in formato .blf della rete CAN in file .csv utilizzabili facilmente da ogni tipo di plotter, come PlotJuggler, tramite un file .dbc.

## Caratteristiche
- **Conversione da BLF a CSV**: Converte i file di log `.blf` in file `.csv`.
- **Conversione da TRC a CSV**: Converte i file di log `.trc` in file `.csv`.
- **Supporto per file DBC**: Utilizza file `.dbc` per interpretare i messaggi CAN.
- **Compatibilità con PlotJuggler**: I file `.csv` generati sono compatibili con PlotJuggler e altri strumenti di plotting.

## Requisiti
- Python 3.x
- Librerie Python: can, csv, dbc, python-can, cantools, tqdm

## Installazione
1. Clona la repository:
    `git clone https://github.com/tuo-username/Converter_BLF_2_CSV.git`
    `cd Converter_BLF_2_CSV`

2. Installa le dipendenze:
    `pip install -r requirements.txt`

## Utilizzo
Posiziona il tuo file `.blf` o `.trc` e i file `.dbc` nella directory del progetto.

Esegui il programma con il seguente comando:

`python convert.py --log tuo_file.blf --dbc tuo_file.dbc`

### Argomenti
- --log: Il percorso del file .blf o .trc da convertire
- --dbc: Il percorso dei file .dbc da utilizzare per l’interpretazione dei messaggi CAN.

## Esempio
### Conversione di un file .blf:
`python converter.py --log log.blf --dbc data_primo.dbc data_secondo.dbc`

### Conversione di un file .trc:
`python converter.py --log log.trc --dbc data_primo.dbc data_secondo.dbc`

## Contributi
I contributi sono benvenuti! Sentiti libero di aprire issue e pull request.

## Licenza
Questo progetto è distribuito sotto la licenza GPL-3.0. Vedi il file LICENSE per maggiori dettagli.
