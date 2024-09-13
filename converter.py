import os
import can
import csv
import cantools
from tqdm import tqdm


def load_dbc_file(dbc_file):
    """Load the DBC file and return the database object."""
    try:
        return cantools.db.load_file(dbc_file, strict=False)
    except Exception as e:
        raise RuntimeError(f"Error loading DBC file '{dbc_file}': {e}")


def extract_signals_from_dbc(db, dbc_file_name):
    """Extract message names and signal names from the DBC database."""
    msg_list = []
    sgn_list = []

    try:
        messages_list = db.messages
        for msg in messages_list:
            for sgn in msg.signal_tree:
                msg_list.append(str(msg.name))
                sgn_list.append(str(sgn))

        return msg_list, sgn_list

    except Exception as e:
        raise RuntimeError(f"Error extracting signals from DBC file '{dbc_file_name}': {e}")


def initialize_output_structure(sgn_list):
    """Initialize the structure for storing the output CSV data."""
    output = [[] for _ in range(len(sgn_list) + 1)]
    for i, sgn in enumerate(sgn_list):
        output[i + 1].append(f"{sgn}")
    current_values = [None] * len(sgn_list)  # Initialize current values for signals
    return output, current_values


def process_blf_file(db, blf_file, msg_list, sgn_list, output, current_values, progress_callback):
    """Process the BLF file and fill in the output structure with decoded signal values."""
    try:
        can_log = can.BLFReader(blf_file)
        first = True
        total_messages = len(list(can_log))  # Get the total number of messages for progress tracking
        can_log = can.BLFReader(blf_file)  # Reset the iterator after counting

        for idx, msg in enumerate(tqdm(can_log, desc=f"Reading signals in {os.path.basename(blf_file)}")):
            try:
                msg_name = db.get_message_by_frame_id(msg.arbitration_id).name
                cur_frame = db.decode_message(msg.arbitration_id, msg.data, decode_choices=False)

                if first:
                    first = False
                    start_abs = msg.timestamp
                    output[0].append("Timestamp")

                output[0].append(msg.timestamp - start_abs)

                value_changed = False  # To track if any value changes in this iteration

                for i in range(len(sgn_list)):
                    if sgn_list[i] in cur_frame and msg_name == msg_list[i]:
                        new_value = cur_frame[sgn_list[i]]
                        if current_values[i] != new_value:
                            current_values[i] = new_value
                            value_changed = True
                        output[i + 1].append(new_value)
                    else:
                        output[i + 1].append(current_values[i])

                if value_changed:
                    progress_callback(idx + 1, total_messages, f"Processing message {idx + 1}/{total_messages}")

            except KeyError:
                pass  # Skip messages not found in the DBC

        progress_callback(100, 100, "Finished reading BLF file")

    except Exception as e:
        raise RuntimeError(f"Error processing BLF file '{blf_file}': {e}")


def write_csv(output, dbc_file, blf_file):
    """Write the output structure to a CSV file with a name based on the DBC and BLF filenames."""
    try:
        dbc_basename = os.path.splitext(os.path.basename(dbc_file))[0]
        blf_basename = os.path.splitext(os.path.basename(blf_file))[0]
        csv_filename = f"{dbc_basename}_{blf_basename}.csv"

        with open(csv_filename, "w", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(zip(*output))

    except Exception as e:
        raise RuntimeError(f"Error writing CSV file: {e}")


def convert_blf_to_csv(dbc_folder, blf_file, progress_callback):
    """Main function to convert a BLF file to multiple CSV files using multiple DBC files."""
    try:
        dbc_files = [os.path.join(dbc_folder, f) for f in os.listdir(dbc_folder) if f.endswith('.dbc')]
        if not dbc_files:
            progress_callback(0, 1, f"No DBC files found in the folder '{dbc_folder}'")
            return

        total_files = len(dbc_files)
        for i, dbc_file in enumerate(dbc_files, start=1):
            progress_callback(i, total_files, f"Processing DBC file {os.path.basename(dbc_file)}")
            db = load_dbc_file(dbc_file)
            msg_list, sgn_list = extract_signals_from_dbc(db, dbc_file)
            output, current_values = initialize_output_structure(sgn_list)
            process_blf_file(db, blf_file, msg_list, sgn_list, output, current_values, progress_callback)
            write_csv(output, dbc_file, blf_file)

        progress_callback(total_files, total_files, "Conversion completed!")
    except Exception as e:
        progress_callback(0, 1, f"Error during conversion: {e}")
