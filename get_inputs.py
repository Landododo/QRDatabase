from QR_counter import count_qr_codes
from tkinter import *
from tkinter import filedialog
from QR_Selector import qr_selector
import pyautogui

def get_inputs():
    """Uses tkinter to prompt the user to select a GDS file"""
    file_path = filedialog.askopenfilename(title = "Select a GDS file",
                                            filetypes=(("gds files","*.gds"),))
    qr_code_count, qr_size, qrs_per_row, qrs_per_col = count_qr_codes(file_path)
    sample_folder = filedialog.askdirectory(title = "Select directory storing sample images")
    print("Reading file: " + file_path.split("/")[-1])
    print("Reading samples from: " + sample_folder)
    qr_selector(qrs_per_row, qrs_per_col)

if __name__ == "__main__":
    get_inputs()
    # gds_file_path = "file.gds"  # Replace with your .gds file path
    # qr_code_count = count_qr_codes(gds_file_path)
    # print(f"Number of QR codes in the GDS file: {qr_code_count}"))