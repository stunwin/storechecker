import tkinter as tk
from tkinter import filedialog, messagebox, Frame, BOTTOM
from PIL import ImageTk, Image
from stores_gui import rangefinder
from feature.nearby_addresses.stores_nearby_addresses import nearby


def rangefinder_launch():
    root.destroy()
    rangefinder()

def nearby_launch():
    root.destroy()
    nearby()


root = tk.Tk()
root.title("Geografy by Something Massive")
main_frame = Frame(root)
main_frame.pack()
b_frame = Frame(root)
b_frame.pack(side = BOTTOM)
root.resizable(False, False)

image = Image.open("header.jpg")
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(main_frame, image=photo)
image_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

rangefinder_button = tk.Button(main_frame, text="rangefinder", command=rangefinder_launch)
rangefinder_button.grid(row=1, column=0, padx=5, pady=5)

nearby_button = tk.Button(main_frame, text="nearby", command=nearby_launch)
nearby_button.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()