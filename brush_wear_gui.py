# Import required modules
import tkinter as tk
from tkinter import ttk
import serial

# Global Varibles
Number_samples = 3
red_first_time = True
blue_first_time = True
green_first_time = True

comm_port = "COM29"  # this is the comm port the scale is connected to

# Serial Port - Change port to match serial port on computer device manager
serialPort = serial.Serial(port=comm_port, baudrate=9600,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)


# Main Window
window = tk.Tk()
window.resizable(width=False, height=False)
window.title("Bursh Wear Testing - Lathe")
window.geometry('1100x300')

# Seperator objects
separator1 = ttk.Separator(window, orient='vertical')
separator1.place(relx=0.33, rely=0, relwidth=0.2, relheight=1)
separator2 = ttk.Separator(window, orient='vertical')
separator2.place(relx=0.66, rely=0, relwidth=0.2, relheight=1)


def Weight_read():

    serialString = ""  # Used to hold data coming over UART
    try:
        serialString = serialPort.readline()
        serialString = serialString.decode('Ascii').strip('+').strip()
        serialString = serialString[:-1]

        return(float(serialString))

    except ValueError:

        # just return 0 Zero if cant be converted to float, and try again
        return(0)


def sample_weight():
    average_weight = []

    for x in range(Number_samples):
        read = Weight_read()
        average_weight.append(read)

    current_weight = Weight_read()
    max_weight = max(average_weight)
    min_weight = min(average_weight)

    loop_count = 0
    while max_weight != min_weight:
        average_weight.pop(0)
        current_weight = Weight_read()
        average_weight.append(current_weight)
        max_weight = max(average_weight)
        min_weight = min(average_weight)
        loop_count += 1

        if loop_count > 25:
            print("check scale!  can't get a stable reading")

    return(current_weight)


def find_num_fibers(fiber_diameter):
    # TODO
    num_fibers = fiber_diameter * 500
    return(num_fibers)


# Label objects
Blue_lbl = ttk.Label(window, text="Blue Brushes",
                     background="blue", font=("Helvetica", 16), width=30)
Blue_lbl.grid(column=0, row=4, rowspan=2, columnspan=5)

Red_lbl = ttk.Label(window, text="Red Brushes",
                    background="red", font=("Helvetica", 16), width=30)
Red_lbl.grid(column=6, row=4, rowspan=2, columnspan=5)

Green_lbl = ttk.Label(window, text="Green Brushes",
                      background="green", font=("Helvetica", 16), width=30)
Green_lbl.grid(column=12, row=4, rowspan=2, columnspan=5)

# Brush tuple Column 0=Item#, 1=Lenth, 2=Fiber Diameter
Brushes = (
    ['Not Measured', 0, 0],
    ['110733-01',  3.00, .010],
    ['110733-02',  3.00, .012],
    ['110733-03',  3.00, .015],
    ['110733-04',  3.19, .010],
    ['110733-05',  3.19, .012],
    ['110733-06',  3.19, .015],
    ['110733-07',  3.25, .010],
    ['110733-08',  3.25, .012],
    ['110733-09',  3.25, .015],
    ['110733-10',  3.34, .010],
    ['110733-11',  3.34, .012],
    ['110733-12',  3.34, .015],
    ['110733-13',  3.47, .010],
    ['110733-14',  3.47, .012],
    ['110733-15',  3.47, .015],
    ['110733-16',  3.53, .012],
    ['110733-17',  3.28, .012],
    ['110733-18',  3.65, .015],
    ['110733-19',  2.32, .008],
    ['110733-20',  2.32, .010],
    ['110733-21',  2.32, .012],
    ['110733-22',  2.50, .010],
    ['110733-23',  2.50, .012],
    ['110733-24',  2.50, .015],
    ['110733-25',  3.88, .012],
    ['110733-26',  3.65, .010],
    ['110733-27',  3.65, .012],
    ['110733-28',  3.65, .019],
    ['110733-29',  4.28, .010])


# Blue Combobox creation
Blue_combo = ttk.Combobox(window)
Blue_combo['values'] = Brushes
Blue_combo.current(1)  # set the selected item
Blue_combo.grid(column=2, row=15)

# Red Combobox creation
Red_combo = ttk.Combobox(window)
Red_combo['values'] = Brushes
Red_combo.current(2)  # set the selected item
Red_combo.grid(column=7, row=15)

# Green Combobox creation
Green_combo = ttk.Combobox(window)
Green_combo['values'] = Brushes
Green_combo.current(3)  # set the selected item
Green_combo.grid(column=13, row=15)


# Selected Blue Brush
def Blue_clicked():
    Blue_Brush = Blue_combo.get()
    print(Blue_Brush)
    print(Blue_start.get())


BlueButton = tk.Button(window, text='Record', command=Blue_clicked)
BlueButton.grid(column=2, row=50)


# Selected Red Brush
def Red_clicked():
    Red_Brush = Red_combo.get()  # sting
    print(Red_Brush)


RedButton = tk.Button(window, text='Record', command=Red_clicked)
RedButton.grid(column=7, row=50)

# #############################################################################
#                                   GREEN BUTTON
# #############################################################################
# Selected Green Brush


def Green_clicked():

    brush_info = Green_combo.get()
    current_weight = sample_weight()
    GreenButton.config(text='Recorded', relief='sunken', command='')

    global green_first_time
    if green_first_time:
        green_first_time = False
        green_fiber_diamter = float(brush_info[-5:])
        find_num_fibers(green_fiber_diamter)
        G_start.set(current_weight)
    else:
  
        G_Current.set(G_Current.get())

    # TODO add command if desired to change
    # Green = sample_weight()
    # G_Previous = Green
    # G_Previous = find_num_fibers()
    # print(G_Previous)
    # print(Green)


GreenButton = tk.Button(window, text='Record', command=Green_clicked)
GreenButton.grid(column=13, row=50)

# Blue labels and Text Boxes
Blue_Start_lbl = ttk.Label(window,
                           text="Start Weight(g)",
                           font=("Helvetica", 12))
Blue_Start_lbl.grid(column=1, row=44,)

B_start = tk.StringVar()
Blue_start = ttk.Entry(window, width=15, textvariable=B_start)
Blue_start.grid(column=2, row=44)

Blue_Previous_lbl = ttk.Label(window,
                              text="Previous Weight(g)",
                              font=("Helvetica", 12))
Blue_Previous_lbl.grid(column=1, row=45,)

B_Previous = tk.StringVar()
Blue_Previous = ttk.Entry(window, width=15, textvariable=B_Previous)
Blue_Previous.grid(column=2, row=45)

Blue_Current_lbl = ttk.Label(window,
                             text="Current Weight(g)",
                             font=("Helvetica", 12))
Blue_Current_lbl.grid(column=1, row=46,)

B_Current = tk.StringVar()
Blue_Current = ttk.Entry(window, width=15, textvariable=B_Current)
Blue_Current.grid(column=2, row=46)

Blue_Diff_lbl = ttk.Label(window,
                          text="Difference Weight (g)",
                          font=("Helvetica", 12))
Blue_Diff_lbl.grid(column=1, row=47,)

B_diff = tk.StringVar()
Blue_diff = ttk.Entry(window, width=15, textvariable=B_diff)
Blue_diff.grid(column=2, row=47)

Blue_wear_lbl = ttk.Label(window,
                          text="Wear (mm)",
                          font=("Helvetica", 12))
Blue_wear_lbl.grid(column=1, row=48)

B_wear = tk.StringVar()
Blue_wear = ttk.Entry(window, width=15, textvariable=B_wear)
Blue_wear.grid(column=2, row=48)

Blue_total_wear_lbl = ttk.Label(window,
                                text="Total Wear (mm)",
                                font=("Helvetica", 12))
Blue_total_wear_lbl.grid(column=1, row=49,)

B_total_wear = tk.StringVar()
Blue_total_wear = ttk.Entry(window, width=15, textvariable=B_total_wear)
Blue_total_wear.grid(column=2, row=49)

# Red labels and Text Boxes
Red_Start_lbl = ttk.Label(window,
                          text="Start Weight(g)",
                          font=("Helvetica", 12))
Red_Start_lbl.grid(column=6, row=44,)

R_start = tk.StringVar()
Red_start = ttk.Entry(window, width=15, textvariable=R_start)
Red_start.grid(column=7, row=44)

Red_Previous_lbl = ttk.Label(window,
                             text="Previous Weight(g)",
                             font=("Helvetica", 12))
Red_Previous_lbl.grid(column=6, row=45,)

R_Previous = tk.StringVar()
Red_Previous = ttk.Entry(window, width=15, textvariable=R_Previous)
Red_Previous.grid(column=7, row=45)

Red_Current_lbl = ttk.Label(window,
                            text="Current Weight(g)",
                            font=("Helvetica", 12))
Red_Current_lbl.grid(column=6, row=46,)

R_Current = tk.StringVar()
Red_Current = ttk.Entry(window, width=15, textvariable=R_Current)
Red_Current.grid(column=7, row=46)

Red_Diff_lbl = ttk.Label(window,
                         text="Difference Weight (g)",
                         font=("Helvetica", 12))
Red_Diff_lbl.grid(column=6, row=47,)

R_diff = tk.StringVar()
Red_diff = ttk.Entry(window, width=15, textvariable=R_diff)
Red_diff.grid(column=7, row=47)

Red_wear_lbl = ttk.Label(window,
                         text="Wear (mm)",
                         font=("Helvetica", 12))
Red_wear_lbl.grid(column=6, row=48)

R_wear = tk.StringVar()
Red_wear = ttk.Entry(window, width=15, textvariable=R_wear)
Red_wear.grid(column=7, row=48)

Red_total_wear_lbl = ttk.Label(window,
                               text="Total Wear (mm)",
                               font=("Helvetica", 12))
Red_total_wear_lbl.grid(column=6, row=49,)

R_total_wear = tk.StringVar()
Red_total_wear = ttk.Entry(window, width=15, textvariable=R_total_wear)
Red_total_wear.grid(column=7, row=49)

# Green labels and Text Boxes
Green_Start_lbl = ttk.Label(window,
                            text="Start Weight(g)",
                            font=("Helvetica", 12))
Green_Start_lbl.grid(column=12, row=44,)

G_start = tk.StringVar()
Green_start = ttk.Entry(window, width=15, textvariable=G_start)
Green_start.grid(column=13, row=44)

Green_Previous_lbl = ttk.Label(window,
                               text="Previous Weight(g)",
                               font=("Helvetica", 12))
Green_Previous_lbl.grid(column=12, row=45,)

G_Previous = tk.StringVar()
Green_Previous = ttk.Entry(window, width=15, textvariable=G_Previous)
Green_Previous.grid(column=13, row=45)

Green_Current_lbl = ttk.Label(window,
                              text="Current Weight(g)",
                              font=("Helvetica", 12))
Green_Current_lbl.grid(column=12, row=46,)

G_Current = tk.StringVar()
Green_Current = ttk.Entry(window, width=15, textvariable=G_Current)
Green_Current.grid(column=13, row=46)

Green_Diff_lbl = ttk.Label(window,
                           text="Difference Weight (g)",
                           font=("Helvetica", 12))
Green_Diff_lbl.grid(column=12, row=47,)

G_diff = tk.StringVar()
Green_diff = ttk.Entry(window, width=15, textvariable=G_diff)
Green_diff.grid(column=13, row=47)

Green_wear_lbl = ttk.Label(window,
                           text="Wear (mm)",
                           font=("Helvetica", 12))
Green_wear_lbl.grid(column=12, row=48)

G_wear = tk.StringVar()
Green_wear = ttk.Entry(window, width=15, textvariable=G_wear)
Green_wear.grid(column=13, row=48)

Green_total_wear_lbl = ttk.Label(window,
                                 text="Total Wear (mm)",
                                 font=("Helvetica", 12))
Green_total_wear_lbl.grid(column=12, row=49,)

G_total_wear = tk.StringVar()
Green_total_wear = ttk.Entry(window, width=15, textvariable=G_total_wear)
Green_total_wear.grid(column=13, row=49)

window.mainloop()
