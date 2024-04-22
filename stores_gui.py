from haversine import haversine, Unit
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, Frame, BOTTOM
from PIL import ImageTk, Image

def select_file1():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        file1_entry.delete(0, tk.END)
        file1_entry.insert(0, file_path)
    update_status()

def select_file2():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        file2_entry.delete(0, tk.END)
        file2_entry.insert(0, file_path)
    update_status()

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)
    update_status()
        
def update_status():
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()
    output_path = output_entry.get()

    if file1_path and file2_path and output_path:
        process_button.config(state="normal")
        status_message.config(text="good to go!", fg="green")
        
    else:
        process_button.config(state="disabled")
        status_message.config(text="please enter two CSV files, and select a save location", fg="grey")

def process_files():
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()
    output_path = output_entry.get()

    target_stores = []
    competitor_stores = []
    total_matches = 0

    # Read csvs file into files

    with open(file2_path, "r", encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            competitor_stores.append(row)
            row["lat"] = float(row["lat"])
            row["lon"] = float(row["lon"])


    with open(file1_path, "r", encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            target_stores.append(row)
            row["lat"] = float(row["lat"])
            row["lon"] = float(row["lon"])
            row["Within 3 Miles"] = 0
            row["Within 5 Miles"] = 0
            row["Within 10 Miles"] = 0
            
    # use haversine formula to calculate distances. tally up matches for each one      
    for c_row in competitor_stores:
        for t_row in target_stores:
            sprouts_location = (c_row["lat"], c_row["lon"])
            wfm_location = (t_row["lat"], t_row["lon"])
            if haversine(sprouts_location, wfm_location, unit = Unit.MILES) < 3:
                t_row["Within 3 Miles"] += 1
            if haversine(sprouts_location, wfm_location, unit = Unit.MILES) < 5:
                t_row["Within 5 Miles"] += 1
            if haversine(sprouts_location, wfm_location, unit = Unit.MILES) < 10:
                t_row["Within 10 Miles"] += 1
                total_matches += 1
            assert t_row["Within 10 Miles"] >= t_row["Within 5 Miles"] >= t_row["Within 3 Miles"], "error at store" + t_row["Street"]

    #write results file        
    with open(output_path, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames = ["Street", "City", "State", "Zip", "lat", "lon", "Within 3 Miles", "Within 5 Miles", "Within 10 Miles" ])
        writer.writeheader()
        for row in target_stores:
            writer.writerow(row)
            
    messagebox.showinfo("Process Complete", "The process has completed successfully!")

def rangefinder():
    #Window setup
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

    #TARGET STORE INPUTS
    file1_label = tk.Label(main_frame, text="Select Target Store CSV:")
    file1_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    file1_entry = tk.Entry(main_frame, width=20)
    file1_entry.grid(row=1, column=1, padx=5, pady=5)

    file1_button = tk.Button(main_frame, text="Browse", command=select_file1)
    file1_button.grid(row=1, column=2, padx=5, pady=5)

    #COMPETITIOR INPUTS
    file2_label = tk.Label(main_frame, text="Select Competitor Store CSV:")
    file2_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

    file2_entry = tk.Entry(main_frame, width=20)
    file2_entry.grid(row=2, column=1, padx=5, pady=5)

    file2_button = tk.Button(main_frame, text="Browse", command=select_file2)
    file2_button.grid(row=2, column=2, padx=5, pady=5)

    #OUTPUT INPUTS
    output_label = tk.Label(main_frame, text="Output File:")
    output_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

    output_entry = tk.Entry(main_frame, width=20)
    output_entry.grid(row=3, column=1, padx=5, pady=5)

    output_button = tk.Button(main_frame, text="Browse", command=select_output_file)
    output_button.grid(row=3, column=2, padx=5, pady=5)

    #PROCESS BUTTON
    process_button = tk.Button(b_frame, text="Process Files", command=process_files, state="disabled")
    process_button.grid(row=0, column=1, padx=1, pady=5)

    #STATUS
    status_message = tk.Label(b_frame, text="please enter two CSV files, and select a save location", fg="grey")
    status_message.grid(row=1, column=1, padx=1, pady=5)

    #BACK BUTTON
    back_button = tk.Button(b_frame, text="back", command=process_files, state="disabled")
    back_button.grid(row=2, column=0, padx=1, pady=5)

    root.mainloop()
    
if __name__ == 'main':
    rangefinder()

