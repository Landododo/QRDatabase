from QR_counter import count_qr_codes
from tkinter import *
from tkinter import filedialog
from QR_Selector import qr_selector
import pyautogui

def get_previous_inputs():
    """Load previous inputs from a input txt file"""
    try:
        with open("user_data.txt", 'r') as f:
            return f.read()
    except:
        return None
    

def get_file_paths():
    """Uses tkinter to prompt the user to select a GDS file"""
    file_path = filedialog.askopenfilename(title = "Select a GDS file",
                                        filetypes=(("gds files","*.gds"),))
    sample_folder = filedialog.askdirectory(title = "Select directory storing sample images")
    with open("user_data.txt", 'w') as f:
        f.write(file_path + "\n" + sample_folder)
    return file_path, sample_folder
def get_inputs():
    previous = get_previous_inputs()
    file_path, sample_folder = None, None
    if previous:
        print(previous)
        file_path, sample_folder = previous.split("\n")
        win = Tk()
        win.geometry("750x250")
        entry= Message(win, text=f"Do you want to proceed with previously inputted gds file {file_path} and sample folder {sample_folder}?", width= 400)
        entry.pack()
        buttons = Frame(win)
        buttons.pack(pady = 5)
        button1= Button(buttons, text= "Yes", command=win.destroy)
        button1.pack(side = LEFT)
        button2= Button(buttons, text= "No", command = lambda: [win.destroy(), get_file_paths()])
        button2.pack()
        win.mainloop()
    else:
        file_path, sample_folder = get_file_paths()

    print(file_path + "checking" + sample_folder)
    qr_code_count, qr_size, qrs_per_row, qrs_per_col = count_qr_codes(file_path)
    print("Reading file: " + file_path.split("/")[-1])
    print("Reading samples from: " + sample_folder)
    qr_selector(qrs_per_row, qrs_per_col)

if __name__ == "__main__":
    get_inputs()
    # gds_file_path = "file.gds"  # Replace with your .gds file path
    # qr_code_count = count_qr_codes(gds_file_path)
    # print(f"Number of QR codes in the GDS file: {qr_code_count}"))