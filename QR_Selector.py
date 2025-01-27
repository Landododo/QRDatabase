import tkinter
from tkinter import *
from PIL import Image, ImageTk
import random


def qr_selector(qrs_per_row, qrs_per_col):
    # Main window
    root = Tk()
    root.title("Interactive QR Code Grid")
    root.geometry("800x600")

    # Scrollable canvas for the QR code grid
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(frame)
    scroll_y = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_x = Scrollbar(frame, orient="horizontal", command=canvas.xview)

    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Bind the mouse wheel and touch pad to scroll
    def on_vertical_scroll(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    def on_horizontal_scroll(event):
        canvas.xview_scroll(-1 * (event.delta // 120), "units")
    canvas.bind_all("<MouseWheel>", on_vertical_scroll)
    canvas.bind_all("<Shift-MouseWheel>", on_horizontal_scroll)

    # Side panel for displaying information
    info_panel = Frame(root, width=200, bg="lightgray")
    info_panel.pack(side=RIGHT, fill=Y)

    info_label = Label(info_panel, text="Select a QR Code", bg="lightgray", wraplength=180)
    info_label.pack(pady=10, padx=10)
    # Simulating QR code click behavior
    def on_qr_click(row, col, bonus):
        info = f"QR Code at Row {row}, Column {col}\nInfo: {bonus}"
        info_label.config(text=info)


    Label(root, text = 'Position image on button', font =('comic sans', 12)).pack(side = TOP, padx =1, pady = 1)
    # Create a photoimage object of the image in the path
    photo = PhotoImage(file = "C:/Users/1108l/OneDrive/Desktop/QR_Database/charlie.png")
    # Resize image to fit on button
    photoimage = photo.subsample(1, 2)
    photo2 = PhotoImage(file = "C:/Users/1108l/OneDrive/Desktop/QR_Database/nate.png")
    photoimage2 = photo2.subsample(1,2)
    # Create a grid of QR code buttons
    rows, cols = qrs_per_row, qrs_per_col  # Large grid size
    for i in range(rows):
        for j in range(cols):
            if (i + j) % 2 == 0:
                qr_button = Button(scrollable_frame, text=f"QR {i},{j}", width=200, height=100,
                                command=lambda r=i, c=j: on_qr_click(r, c, "CHARLIE"), image=photoimage)
                qr_button.grid(row=i, column=j, padx=1, pady=1)
            else:
                qr_button = Button(scrollable_frame, text=f"QR {i},{j}", width=200, height=100,
                                command=lambda r=i, c=j: on_qr_click(r, c, "NATE"), image=photoimage2)
                qr_button.grid(row=i, column=j, padx=1, pady=1)
    root.mainloop()

if __name__=="__main__":
    qr_selector(20, 60)



