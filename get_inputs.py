from QR_counter import count_qr_codes
from tkinter import *
from tkinter import filedialog
import pyautogui


def open_file():
    file_path = filedialog.askopenfilename(title = "File Selector",
                                           filetypes=(("gds files","*.gds"),
                                            ("all files","*.*")))
window = Tk()
button = Button(text= "Open", command= open_file)
button.pack()
window.mainloop()

if __name__ == "__main__":
    gds_file_path = "file.gds"  # Replace with your .gds file path
    qr_code_count = count_qr_codes(gds_file_path)
    print(f"Number of QR codes in the GDS file: {qr_code_count}")