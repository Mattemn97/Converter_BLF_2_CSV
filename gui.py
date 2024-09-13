import threading
from tkinter import Tk, filedialog, Label, Button, StringVar, messagebox, ttk
from converter import convert_blf_to_csv

def select_log_file(log_path_var):
    """Open a file dialog to select the log file."""
    log_file = filedialog.askopenfilename(
        title="Select the .blf log file",
        filetypes=[("BLF files", "*.blf")]
    )
    log_path_var.set(log_file)


def select_dbc_folder(dbc_folder_var):
    """Open a folder dialog to select the folder with DBC files."""
    dbc_folder = filedialog.askdirectory(title="Select the folder with DBC files")
    dbc_folder_var.set(dbc_folder)


def run_conversion_thread(dbc_folder, blf_file, progress_bar, status_label_var):
    """Run the conversion in a separate thread to avoid blocking the GUI."""
    def update_progress(current, total, status):
        """Update progress bar and status label."""
        progress_bar['value'] = (current / total) * 100
        status_label_var.set(status)  # Update the status label with current status

    # Run the conversion process in a thread
    threading.Thread(target=convert_blf_to_csv, args=(dbc_folder, blf_file, update_progress)).start()


def create_gui():
    """Create the GUI for the converter."""
    root = Tk()
    root.title("BLF to CSV Converter")

    log_path_var = StringVar()
    dbc_folder_var = StringVar()
    status_label_var = StringVar()  # StringVar to update the status label dynamically

    Label(root, text="Select BLF Log File:").grid(row=0, column=0, padx=10, pady=10)
    Label(root, text="Select DBC Folder:").grid(row=1, column=0, padx=10, pady=10)

    log_entry = Label(root, textvariable=log_path_var, width=50, anchor="w")
    log_entry.grid(row=0, column=1, padx=10, pady=10)

    dbc_entry = Label(root, textvariable=dbc_folder_var, width=50, anchor="w")
    dbc_entry.grid(row=1, column=1, padx=10, pady=10)

    Button(root, text="Browse", command=lambda: select_log_file(log_path_var)).grid(row=0, column=2, padx=10, pady=10)
    Button(root, text="Browse", command=lambda: select_dbc_folder(dbc_folder_var)).grid(row=1, column=2, padx=10, pady=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=2, column=0, padx=10, pady=10)

    # Label to show what the program is currently doing or if there are errors
    status_label = Label(root, textvariable=status_label_var, width=50, anchor="w")
    status_label.grid(row=2, column=1, padx=10, pady=10)

    Button(root, text="Start Conversion", command=lambda: run_conversion_thread(
        dbc_folder_var.get(), log_path_var.get(), progress_bar, status_label_var)).grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()
