import can
import csv
import cantools
import pandas as pd
from tqdm import tqdm


print("Segui attentamente le indicazioni altrimenti si sputtana tutto <3")
file_dbc = str(input("Inserisci il path del file .dbc, includendo l'estensione e la doppia \\ nel foldering: \n"))
file_blf = str(input("Inserisci il path del file .blf, includendo l'estensione e la doppia \\ nel foldering: \n"))
file_csv = str(input("Inserisci il path del file .csv, includendo l'estensione e la doppia \\ nel foldering: \n"))

list_msg_out = []
list_sgn_out = []

db = cantools.db.load_file(file_dbc, strict=False)
can_log = can.BLFReader(file_blf)

lista_messaggi = db.messages

for msg in tqdm(lista_messaggi, desc="Leggendo i segnali nel .dbc"):
    for sgn in msg.signal_tree:
        list_msg_out.append(str(msg.name))
        list_sgn_out.append(str(sgn))

output = [[] for i in range(len(list_sgn_out)+1)]
first = True

for i in range(0,len(list_sgn_out)):
    output[i+1].append(list_msg_out[i] + " :-: " + list_sgn_out[i])
    
for msg in tqdm(can_log, desc="Leggendo i segnali nel .blf"):
    try:
        msg_name = db.get_message_by_frame_id(msg.arbitration_id).name
        cur_frame = db.decode_message(msg.arbitration_id, msg.data, decode_choices=False)
        if first: 
            first = False
            start_abs = msg.timestamp
            output[0].append("Timestamp")
        else:
            output[0].append(msg.timestamp-start_abs)
        if bool(set(list_sgn_out) & set(cur_frame)):
            for i in range(0,len(list_sgn_out)):
                if list_sgn_out[i] in cur_frame and msg_name == list_msg_out[i]:
                    output[i+1].append(cur_frame[list_sgn_out[i]])
                else:
                    output[i+1].append('')
    except:
        pass

output = zip(*output)
print("Creando file .csv")
with open(file_csv, "w", newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows(output)
