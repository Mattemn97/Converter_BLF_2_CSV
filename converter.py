import argparse
import os
import can
import csv
import cantools
from tqdm import tqdm


def load_dbc_file(dbc_file):
    """Load the DBC file and return the database object."""
    return cantools.db.load_file(dbc_file, strict=False)


def extract_signals_from_dbc(db, dbc_file_name):
    """Extract message names and signal names from the DBC database."""
    msg_list = []
    sgn_list = []

    messages_list = db.messages
    for msg in tqdm(messages_list, desc=f"Reading signals in {os.path.basename(dbc_file_name)}"):
        for sgn in msg.signal_tree:
            msg_list.append(str(msg.name))
            sgn_list.append(str(sgn))

    return msg_list, sgn_list


def initialize_output_structure(sgn_list):
    """Initialize the structure for storing the output CSV data and signal values."""
    output = [[] for _ in range(len(sgn_list) + 1)]
    current_values = [0] * len(sgn_list)  # Inizializziamo tutti i segnali a 0
    for i, sgn in enumerate(sgn_list):
        output[i + 1].append(f"{sgn}")
    return output, current_values


def process_blf_file(db, blf_file, msg_list, sgn_list, output, current_values):
    """Process the BLF file and fill in the output structure with decoded signal values."""
    can_log = can.BLFReader(blf_file)
    first = True
    previous_values = current_values.copy()  # Memorizziamo i valori precedenti

    for msg in tqdm(can_log, desc=f"Reading signals in {os.path.basename(blf_file)}"):
        try:
            msg_name = db.get_message_by_frame_id(msg.arbitration_id).name
            cur_frame = db.decode_message(msg.arbitration_id, msg.data, decode_choices=False)

            if first:
                first = False
                start_abs = msg.timestamp
                output[0].append("Timestamp")

            timestamp = msg.timestamp - start_abs
            row = [timestamp]  # Start with timestamp
            has_changes = False  # Flag per tracciare i cambiamenti nei segnali

            # Aggiorniamo i valori correnti dei segnali e controlliamo se ci sono cambiamenti
            for i in range(len(sgn_list)):
                if sgn_list[i] in cur_frame and msg_name == msg_list[i]:
                    current_value = cur_frame[sgn_list[i]]
                    if current_value != previous_values[i]:
                        current_values[i] = current_value  # Aggiorniamo solo se il valore è cambiato
                        has_changes = True  # Flag indica cambiamento
                row.append(current_values[i])

            if has_changes:  # Scriviamo solo se c'è stato un cambiamento nei valori dei segnali
                previous_values = current_values.copy()  # Aggiorniamo i valori precedenti
                for i in range(len(row)):
                    output[i].append(row[i])

        except KeyError:
            pass

    return output


def write_csv(output, dbc_file, blf_file):
    """Write the output structure to a CSV file with a name based on the DBC and BLF filenames."""
    dbc_basename = os.path.splitext(os.path.basename(dbc_file))[0]
    blf_basename = os.path.splitext(os.path.basename(blf_file))[0]
    csv_filename = f"{dbc_basename}_{blf_basename}.csv"

    print(f"Creating {csv_filename}")
    with open(csv_filename, "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(zip(*output))


def convert_blf_to_csv(dbc_files, blf_file):
    """Main function to convert a BLF file to multiple CSV files using multiple DBC files."""
    for dbc_file in dbc_files:
        db = load_dbc_file(dbc_file)
        msg_list, sgn_list = extract_signals_from_dbc(db, dbc_file)
        output, current_values = initialize_output_structure(sgn_list)
        output = process_blf_file(db, blf_file, msg_list, sgn_list, output, current_values)
        write_csv(output, dbc_file, blf_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert BLF files to CSV using one or more DBC files.")
    parser.add_argument("--blf", required=True, help="The path to the .blf file to convert.")
    parser.add_argument("--dbc", required=True, nargs='+',
                        help="The path(s) to the .dbc file(s) used for interpreting CAN messages.")

    args = parser.parse_args()

    convert_blf_to_csv(args.dbc, args.blf)
