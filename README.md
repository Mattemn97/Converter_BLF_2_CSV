# Converter_BLF_2_CSV
Questo programma converte i file di log in formato .blf della rete CAN in file .csv utilizzabili facilmente da ogni tipo di plotter, come PlotJuggler, tramite un file .dbc.

## Caratteristiche
- Conversione da BLF a CSV: Converte i file di log .blf in file .csv.
- Supporto per file DBC: Utilizza un file .dbc per interpretare i messaggi CAN.
- Compatibilità con PlotJuggler: I file .csv generati sono compatibili con PlotJuggler e altri strumenti di plotting.

## Requisiti
- Python 3.x
- Librerie Python: can, csv, dbc

## Installazione
1. Clona la repository:
    `git clone https://github.com/tuo-username/Converter_BLF_2_CSV.git`
    `cd Converter_BLF_2_CSV`

2. Installa le dipendenze:
    `pip install -r requirements.txt`

## Utilizzo
Posiziona il tuo file .blf e il file .dbc nella directory del progetto.

Esegui il programma con il seguente comando:

`python convert.py --blf tuo_file.blf --dbc tuo_file.dbc --csv output.csv`

### Argomenti
- --blf: Il percorso del file .blf da convertire.
- --dbc: Il percorso del file .dbc da utilizzare per l’interpretazione dei messaggi CAN.
- --csv: Il percorso del file .csv di output.

## Esempio
`python convert.py --blf logs.blf --dbc database.dbc --csv output.csv`

## Contributi
I contributi sono benvenuti! Sentiti libero di aprire issue e pull request.

## Licenza
Questo progetto è distribuito sotto la licenza GPL-3.0. Vedi il file LICENSE per maggiori dettagli.