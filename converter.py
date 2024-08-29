import argparse
import can
import csv
import cantools
from tqdm import tqdm


def load_dbc_file(dbc_file):
    """Load the DBC file and return the database object."""
    return cantools.db.load_file(dbc_file, strict=False)


def extract_signals_from_dbc(db):
    """Extract message names and signal names from the DBC database."""
    msg_list = []
    sgn_list = []

    messages_list = db.messages
    for msg in tqdm(messages_list, desc="Reading signals in .dbc"):
        for sgn in msg.signal_tree:
            msg_list.append(str(msg.name))
            sgn_list.append(str(sgn))

    return msg_list, sgn_list


def initialize_output_structure(sgn_list):
    """Initialize the structure for storing the output CSV data."""
    output = [[] for _ in range(len(sgn_list) + 1)]
    for i, sgn in enumerate(sgn_list):
        output[i + 1].append(f"{sgn}")

    return output


def process_blf_file(db, blf_file, msg_list, sgn_list, output):
    """Process the BLF file and fill in the output structure with decoded signal values."""
    can_log = can.BLFReader(blf_file)
    first = True

    for msg in tqdm(can_log, desc="Reading signals in .blf"):
        try:
            msg_name = db.get_message_by_frame_id(msg.arbitration_id).name
            cur_frame = db.decode_message(msg.arbitration_id, msg.data, decode_choices=False)
            if first:
                first = False
                start_abs = msg.timestamp
                output[0].append("Timestamp")
            else:
                output[0].append(msg.timestamp - start_abs)

            for i in range(len(sgn_list)):
                if sgn_list[i] in cur_frame and msg_name == msg_list[i]:
                    output[i + 1].append(cur_frame[sgn_list[i]])
                else:
                    output[i + 1].append('')

        except KeyError:
            pass

    return output


def write_csv(output, csv_file):
    """Write the output structure to a CSV file."""
    print("Creating .csv file")
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(zip(*output))


def convert_blf_to_csv(dbc_file, blf_file, csv_file):
    """Main function to convert a BLF file to a CSV file using a DBC file."""
    db = load_dbc_file(dbc_file)
    msg_list, sgn_list = extract_signals_from_dbc(db)
    output = initialize_output_structure(sgn_list)
    output = process_blf_file(db, blf_file, msg_list, sgn_list, output)
    write_csv(output, csv_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert BLF files to CSV using a DBC file.")
    parser.add_argument("--blf", required=True, help="The path to the .blf file to convert.")
    parser.add_argument("--dbc", required=True, help="The path to the .dbc file used for interpreting CAN messages.")
    parser.add_argument("--csv", required=True, help="The path to the output .csv file.")

    args = parser.parse_args()

    convert_blf_to_csv(args.dbc, args.blf, args.csv)
