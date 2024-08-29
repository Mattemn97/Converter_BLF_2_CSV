import argparse
import can
import csv
import cantools
from tqdm import tqdm


def convert_blf_to_csv(dbc_file, blf_file, csv_file):
    msg_list = []
    sgn_list = []

    db = cantools.db.load_file(dbc_file, strict=False)
    can_log = can.BLFReader(blf_file)

    messages_list = db.messages

    for msg in tqdm(messages_list, desc="Reading signals in .dbc"):
        for sgn in msg.signal_tree:
            msg_list.append(str(msg.name))
            sgn_list.append(str(sgn))

    output = [[] for _ in range(len(sgn_list) + 1)]
    first = True

    for i in range(len(sgn_list)):
        output[i + 1].append(f"{msg_list[i]} :-: {sgn_list[i]}")

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
            if set(sgn_list) & set(cur_frame):
                for i in range(len(sgn_list)):
                    if sgn_list[i] in cur_frame and msg_name == msg_list[i]:
                        output[i + 1].append(cur_frame[sgn_list[i]])
                    else:
                        output[i + 1].append('')
        except:
            pass

    output = zip(*output)
    print("Creating .csv file")
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert BLF files to CSV using a DBC file.")
    parser.add_argument("--blf", required=True, help="The path to the .blf file to convert.")
    parser.add_argument("--dbc", required=True, help="The path to the .dbc file used for interpreting CAN messages.")
    parser.add_argument("--csv", required=True, help="The path to the output .csv file.")

    args = parser.parse_args()

    convert_blf_to_csv(args.dbc, args.blf, args.csv)
