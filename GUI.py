#### This script is to be run first, to set the parameters for the tool ####
#### Paste the file path of your "main" file on line 169 ####

import tkinter as tk
from tkinter import ttk

# This file is used to set the parameters to be used in the main script. Just press run!!


def button_function(user_number):
    value = user_number.get()
    return value


def close_window(window_name):
    window_name.destroy()


def user_interface():

    window = tk.Tk()
    window.geometry("500x700")
    window.title("")

    title = tk.Label(window, text="ML IMAGE GENERATION UI", font=("Arial", 18))
    title.pack(padx=20, pady=20)

    # Create frame for buttons to go in
    button_frame = tk.Frame(window)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    # Create labels  - Create class for this
    label_1 = tk.Label(button_frame, text="Number of Angles", font=("Arial", 18))
    label_1.grid(row=1, column=0, padx=10, sticky=tk.W + tk.E)

    label_2 = tk.Label(button_frame, text="Number of Axes", font=("Arial", 18))
    label_2.grid(row=4, column=0, padx=10, sticky=tk.W + tk.E)

    label_3 = tk.Label(button_frame, text="Distance", font=("Arial", 18))
    label_3.grid(row=7, column=0, padx=10, sticky=tk.W + tk.E)

    label_4 = tk.Label(button_frame, text="Object Texture", font=("Arial", 18))
    label_4.grid(row=10, column=0, padx=10, sticky=tk.W + tk.E)

    label_5 = tk.Label(button_frame, text="Background", font=("Arial", 18))
    label_5.grid(row=13, column=0, padx=10, sticky=tk.W + tk.E)

    label_6 = tk.Label(button_frame, text="Lighting", font=("Arial", 18))
    label_6.grid(row=16, column=0, padx=10, sticky=tk.W + tk.E)

    label_7 = tk.Label(button_frame, text="Resolution", font=("Arial", 18))
    label_7.grid(row=19, column=0, padx=10, sticky=tk.W + tk.E)

    label_8 = tk.Label(button_frame, text="Object Postion", font=("Arial", 18))
    label_8.grid(row=22, column=0, padx=10, sticky=tk.W + tk.E)

    # Create Textbox(s) - Create class for this
    entry_number_1 = tk.IntVar(value=3)
    entry_1 = ttk.Entry(button_frame, textvariable=entry_number_1)
    entry_1.grid(row=1, column=1, padx=30, sticky=tk.W + tk.E)

    entry_number_2 = tk.IntVar(value=3)
    entry_2 = ttk.Entry(button_frame, textvariable=entry_number_2)
    entry_2.grid(row=4, column=1, padx=30, sticky=tk.W + tk.E)

    entry_number_3 = tk.IntVar(value=1)
    entry_3 = ttk.Entry(button_frame, textvariable=entry_number_3)
    entry_3.grid(row=7, column=1, padx=30, sticky=tk.W + tk.E)

    entry_number_4 = tk.IntVar(value=1)
    entry_4 = ttk.Entry(button_frame, textvariable=entry_number_4)
    entry_4.grid(row=10, column=1, padx=30, sticky=tk.W + tk.E)

    entry_number_5 = tk.IntVar(value=1)
    entry_5 = ttk.Entry(button_frame, textvariable=entry_number_5)
    entry_5.grid(row=13, column=1, padx=30, sticky=tk.W + tk.E)

    entry_number_6 = tk.IntVar(value=1)
    entry_6 = ttk.Entry(button_frame, textvariable=entry_number_6)
    entry_6.grid(row=16, column=1, padx=30, sticky=tk.W + tk.E)

    entry_number_7 = tk.IntVar(value=1)
    entry_7 = ttk.Entry(button_frame, textvariable=entry_number_7)
    entry_7.grid(row=19, column=1, padx=30, sticky=tk.W + tk.E)

    entry_number_8 = tk.IntVar(value=1)
    entry_8 = ttk.Entry(button_frame, textvariable=entry_number_8)
    entry_8.grid(row=22, column=1, padx=30, sticky=tk.W + tk.E)

    # Create Itallic warnings above Textbox(s)
    label_1 = tk.Label(button_frame, text="(max = 10)", font=("Arial italic", 15))
    label_1.grid(row=0, column=1, padx=30, sticky="w")

    label_2 = tk.Label(button_frame, text="(max = 30)", font=("Arial italic", 15))
    label_2.grid(row=3, column=1, padx=30, sticky="w")

    label_3 = tk.Label(button_frame, text="(1=Y or 0=N)", font=("Arial italic", 15))
    label_3.grid(row=6, column=1, padx=30, sticky="w")

    label_4 = tk.Label(button_frame, text="(1=Y or 0=N)", font=("Arial italic", 15))
    label_4.grid(row=9, column=1, padx=30, sticky="w")

    label_5 = tk.Label(button_frame, text="(1=Y or 0=N)", font=("Arial italic", 15))
    label_5.grid(row=12, column=1, padx=30, sticky="w")

    label_6 = tk.Label(button_frame, text="(1=Y or 0=N)", font=("Arial italic", 15))
    label_6.grid(row=15, column=1, padx=30, sticky="w")

    label_7 = tk.Label(button_frame, text="(0=1080, 1=720, 2=540, 3=YOLO)", font=("Arial italic", 15))
    label_7.grid(row=18, column=1, padx=30, sticky="w")

    label_8 = tk.Label(button_frame, text="(1=Y or 0=N)", font=("Arial italic", 15))
    label_8.grid(row=21, column=1, padx=30, sticky="w")

    # Create blank rows
    gap_1 = tk.Label(button_frame, text=" ", )
    gap_1.grid(row=2, column=1, )

    gap_2 = tk.Label(button_frame, text=" ", )
    gap_2.grid(row=5, column=1, )

    gap_3 = tk.Label(button_frame, text=" ", )
    gap_3.grid(row=8, column=1, )

    gap_4 = tk.Label(button_frame, text=" ", )
    gap_4.grid(row=11, column=1, )

    gap_5 = tk.Label(button_frame, text=" ", )
    gap_5.grid(row=14, column=1, )

    gap_6 = tk.Label(button_frame, text=" ", )
    gap_6.grid(row=17, column=1, )

    gap_7 = tk.Label(button_frame, text=" ", )
    gap_7.grid(row=20, column=1, )

    # Exit Button
    button = tk.ttk.Button(window, text="Submit", command=lambda: close_window(window))
    button.pack(side=tk.BOTTOM, pady=15)

    # Insert the frame
    button_frame.pack()

    # run
    window.mainloop()

    inputs = []
    
    inputs.append(button_function(entry_number_1))
    inputs.append(button_function(entry_number_2))
    inputs.append(button_function(entry_number_3))
    inputs.append(button_function(entry_number_4))
    inputs.append(button_function(entry_number_5))
    inputs.append(button_function(entry_number_6))
    inputs.append(button_function(entry_number_7))
    inputs.append(button_function(entry_number_8))

    return inputs


def Params_file(parameters):
    data_file = open(main_folder + "Images/" + "parameters.txt", "w")
    for pars in parameters:
        data_file.write(f"{pars}\n")
    data_file.close()

#### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Paste the location of the mail folder here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#####

main_folder = "/Users/mgbuck/Desktop/Blender Programming/"

#### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Paste the location of the mail folder here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#####

entries = user_interface()
Params_file(entries)




