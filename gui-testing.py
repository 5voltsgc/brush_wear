
# Import required modules
import tkinter as tk
from tkinter import ttk, messagebox

import datetime

# Global Varibles
Number_samples = 3
loop_count = 1
red_first_time = True
blue_first_time = True
green_first_time = True
red_recorded = True  # TODO this should be True but testing
blue_recorded = False  # TODO this should be True but testing
green_recorded = False

filename = ("Brush_wear" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") +
            ".csv")

# '[0] item Number',
# '[1] Fiber Count',
# '[2] Fiber Radius',
# '[3] Start Length',
# '[4] Start weight',
# '[5] Current weight',
# '[6] Diff from Previous weight',
# '[7] Current Length'

green_brush = ['[0] item Number',
               '[1] Fiber Count',
               '[2] Fiber Radius',
               '[3] Start Length',
               '[4] Start weight',
               '[5] Current weight',
               '[6] Diff from Previous weight',
               '[7] Current Length'
               ]
red_brush = ['[0] item Number',
             '[1] Fiber Count',
             '[2] Fiber Radius',
             '[3] Start Length',
             '[4] Start weight',
             '[5] Current weight',
             '[6] Diff from Previous weight',
             '[7] Current Length'
             ]

blue_brush = ['[0] item Number',
              '[1] Fiber Count',
              '[2] Fiber Radius',
              '[3] Start Length',
              '[4] Start weight',
              '[5] Current weight',
              '[6] Diff from Previous weight',
              '[7] Current Length'
              ]

# Main Window
window = tk.Tk()
window.resizable(width=False, height=False)
window.title("Bursh Wear Testing - Lathe")
window.geometry('1100x300')

# Seperator objects
separator1 = ttk.Separator(window, orient='vertical')
separator1.place(relx=0.33, rely=0, relwidth=0.2, relheight=.75)
separator2 = ttk.Separator(window, orient='vertical')
separator2.place(relx=0.66, rely=0, relwidth=0.2, relheight=.75)
separator3 = ttk.Separator(window, orient='horizontal')
separator3.place(relx=0, rely=.67, relwidth=1, relheight=.75)


def find_fiber_count(scale, fiber_radius=0.127, fiber_height=76.2,
                     collar=2.213479):
    """    Find Fiber Count, this function returns the estimated count of fibers.
    This is calculated by following these steps:
    Step 1. find weight of all fibers by subtracting the collar weight from
            Scale weight or 2.213479 grams.
    Step 2. Calculate weight of one fiber = pi() * radius^2 * height * Desity
    Step 3. Divide fibers weight from step one by weight of one fiber step 2.
    Step 4. Return the value from step 3. as an integer rounded up.

    The density of AISI C1018 & C1065 is 0.00787(g/mm³) gram/mm³
    The collar is precalculated to be 2.213479 grams
    """
    # Step 1 - Find weight of all fibers
    fibers_weight = scale - collar

    # Step 2 - weight of one fiber
    fiber_weight = 3.141592 * fiber_radius**2 * fiber_height * 0.00787

    # Step 3 - Divide weight of all fibers by weight of one fiber to find count
    count = int(round(fibers_weight / fiber_weight, 0))

    return(count)


def sample_weight():
    return(31.3)


def find_height(scale, fiber_radius=0.127, Num_fibers=974, collar=2.213479):
    """
    Find height returns the estimated height of the brush based on count of
    fibers, radius of one fiber, and scale weight following these steps:
    Step 1. find weight of all fibers by subtracting the collar weight from
            Scale weight or 2.213479 grams.
    Step 2. Divide weight by num_fibers to get weight of one fiber
    Step 3. Solve for height = one fiber weight/ pi() * r^2 *density
    Step 4. Return th height of the fibers


    The density of AISI C1018 & C1065 is 0.00787(g/mm³) gram/mm³
    The collar is precalculated to be 2.213479 grams
    """

    # Step 1. Find weight of all fibers
    fibers_weight = scale - collar

    # Step 2. Find weight of one fiber
    fiber_weight = fibers_weight / Num_fibers

    # Step 3. Solve for height of one fiber
    height = round(fiber_weight / (3.141592 * fiber_radius**2 * 0.00787), 8)
    return(height)


def record_complete():
    """
    This function resets the buttons so a new record can be created
    it compiles all the data and writes to a file
    erases the notes text entry, updates the odometer
    """
    global Green_Recorded
    global Blue_Recorded
    global Red_recoded
    global loop_count  # TODO Loop_count needs to be distance and add odometer

    Green_Recorded = False
    Blue_Recorded = False
    Red_recoded = False
    print('Completed was executed')
    green = ', '.join([str(elem) for elem in green_brush])
    red = ', '.join([str(elem) for elem in red_brush])
    blue = ', '.join([str(elem) for elem in red_brush])

    record_data = (str(datetime.datetime.now())
                   + ", "
                   + str(loop_count)
                   + ", "
                   + green
                   + ", "
                   + red
                   + ", "
                   + blue)

    print(record_data)

    with open(filename, 'a') as f:

        loop_count += 1
        f.write(record_data)
        f.write('\n')
        f.close
        print(record_data)
        record_data = ""


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
    ['110733-01', 76.2, 0.254],
    ['110733-02', 76.2, 0.3048],
    ['110733-03', 76.2, 0.381],
    ['110733-04', 81.026, 0.254],
    ['110733-05', 81.026, 0.3048],
    ['110733-06', 81.026, 0.381],
    ['110733-07', 82.55, 0.254],
    ['110733-08', 82.55, 0.3048],
    ['110733-09', 82.55, 0.381],
    ['110733-10', 84.836, 0.254],
    ['110733-11', 84.836, 0.3048],
    ['110733-12', 84.836, 0.381],
    ['110733-13', 88.138, 0.254],
    ['110733-14', 88.138, 0.3048],
    ['110733-15', 88.138, 0.381],
    ['110733-16', 89.662, 0.3048],
    ['110733-17', 83.312, 0.3048],
    ['110733-18', 92.71, 0.381],
    ['110733-19', 58.928, 0.2032],
    ['110733-20', 58.928, 0.254],
    ['110733-21', 58.928, 0.3048],
    ['110733-22', 63.5, 0.254],
    ['110733-23', 63.5, 0.3048],
    ['110733-24', 63.5, 0.381],
    ['110733-25', 98.552, 0.3048],
    ['110733-26', 92.71, 0.254],
    ['110733-27', 92.71, 0.3048],
    ['110733-28', 92.71, 0.4826],
    ['110733-29', 108.712, 0.254],)

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


BlueButton = tk.Button(window, text='Record', font=("Helvetica", 12),
                       command=Blue_clicked)
BlueButton.grid(column=2, row=50)


# Selected Red Brush
def Red_clicked():
    Red_Brush = Red_combo.get()  # sting
    print(Red_Brush)


RedButton = tk.Button(window, text='Record', command=Red_clicked,
                      font=("Helvetica", 12))
RedButton.grid(column=7, row=50,)

# #############################################################################
#                                   GREEN BUTTON
# #############################################################################
# Selected Green Brush


def Green_clicked():
    """
    This function will be repeated for the other two buttons.
    Collect information: Scale weight, Brush info, previous weight, and do the
    calculations. Format this data for the tkinter GUI, and the output file.
    """
    global green_first_time
    global green_brush
    global green_recorded

    green_recorded = True

    # Change button to be sunken
    GreenButton.config(text='Recorded', relief='sunken')

    # Get the current weight from the scale
    current_weight = sample_weight()

    # Find out if this is the first record
    if green_first_time:
        green_first_time = False

        # Read the selected brush then make it grayed out
        brush_info = Green_combo.get()
        Green_combo.config(state="disabled")

        # [0] Item number
        green_brush[0] = brush_info[:9]

        # [2] Fiber Radius
        green_brush[2] = float(brush_info[-5:])/2

        # [3] Start length - slice [start:end]
        green_brush[3] = float(brush_info[10:14].strip())

        # [1] fiber Count
        green_brush[1] = find_fiber_count(current_weight,
                                          green_brush[2],
                                          green_brush[3]
                                          )

        # [4] Start Weight
        green_brush[4] = current_weight
        G_start.set(green_brush[4])

        # [5] Current weight
        green_brush[5] = current_weight
        G_Current.set(green_brush[5])

        # [6] Diff from Previous weight
        green_brush[6] = current_weight
        G_Previous.set(green_brush[6])
        G_diff.set(0.00)

        # [7] Current Length
        green_brush[7] = green_brush[3]
        G_est_length.set(green_brush[7])

    else:
        # TODO remove this line - testing green_brush[7] is set in first_time
        green_brush[7] = 30.0

        # update the previous entry widget
        G_Previous.set(green_brush[7])

        # [6] update the difference list and text widget
        green_brush[6] = "{:.4f}".format((green_brush[7]) - current_weight)
        G_diff.set(green_brush[6])

        # [5] Current weight
        green_brush[5] = current_weight
        G_Current.set(green_brush[5])

        # [7] update Current length
        green_brush[7] = "{:.4f}".format(find_height(current_weight))
        G_est_length.set(green_brush[7])

    # Have all colors been recorded, if so complete record

    # print(green_recorded)  # TODO remove this after testing
    # print(blue_recorded)  # TODO remove this after testing
    # print(red_recorded)  # TODO remove this after testing

    if green_recorded and blue_recorded and red_recorded:
        record_complete()


GreenButton = tk.Button(window, text='Record', font=("Helvetica", 12),
                        command=Green_clicked)
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

Blue_est_length_lbl = ttk.Label(window,
                                text="Est. Length (mm)",
                                font=("Helvetica", 12))
Blue_est_length_lbl.grid(column=1, row=48,)

B_est_length = tk.StringVar()
Blue_est_length = ttk.Entry(window, width=15, textvariable=B_est_length)
Blue_est_length.grid(column=2, row=48)

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

Red_est_length_lbl = ttk.Label(window,
                               text="Est. Length (mm)",
                               font=("Helvetica", 12))
Red_est_length_lbl.grid(column=6, row=48,)

R_est_length = tk.StringVar()
Red_est_length = ttk.Entry(window, width=15, textvariable=R_est_length)
Red_est_length.grid(column=7, row=48)

# Green labels and Text Boxes
Green_Start_lbl = ttk.Label(window,
                            text="Start Weight(g)",
                            font=("Helvetica", 12))
Green_Start_lbl.grid(column=12, row=44,)

G_start = tk.StringVar()
Green_start = ttk.Entry(window,
                        width=15,
                        textvariable=G_start,
                        state='readonly',
                        font=("Helvetica", 12),
                        justify='center'
                        )
Green_start.grid(column=13, row=44)

Green_Previous_lbl = ttk.Label(window,
                               text="Previous Weight(g)",
                               font=("Helvetica", 12)
                               )
Green_Previous_lbl.grid(column=12, row=45,)

G_Previous = tk.StringVar()
Green_Previous = ttk.Entry(window,
                           width=15,
                           textvariable=G_Previous,
                           state='readonly',
                           font=("Helvetica", 12),
                           justify='center'
                           )
Green_Previous.grid(column=13, row=45)

Green_Current_lbl = ttk.Label(window,
                              text="Current Weight(g)",
                              font=("Helvetica", 12))
Green_Current_lbl.grid(column=12, row=46,)

G_Current = tk.StringVar()
Green_Current = ttk.Entry(window,
                          width=15,
                          textvariable=G_Current,
                          state='readonly',
                          font=("Helvetica", 12),
                          justify='center'
                          )
Green_Current.grid(column=13, row=46)

Green_Diff_lbl = ttk.Label(window,
                           text="Difference Weight (g)",
                           font=("Helvetica", 12))
Green_Diff_lbl.grid(column=12, row=47,)

G_diff = tk.StringVar()
Green_diff = ttk.Entry(window,
                       width=15,
                       textvariable=G_diff,
                       state='readonly',
                       font=("Helvetica", 12),
                       justify='center')
Green_diff.grid(column=13, row=47)

Green_est_length_lbl = ttk.Label(window,
                                 text="Est. Length (mm)",
                                 font=("Helvetica", 12))
Green_est_length_lbl.grid(column=12, row=48,)

G_est_length = tk.StringVar()
Green_est_length = ttk.Entry(window,
                             width=15,
                             textvariable=G_est_length,
                             state='readonly',
                             font=("Helvetica", 12),
                             justify='center')
Green_est_length.grid(column=13, row=48)

# The record number label and entry
record_lbl = ttk.Label(window,
                       text="Record #",
                       font=("Helvetica", 12))
record_lbl.place(relx=.1, rely=.70,)

record_num = tk.StringVar()
record_num = ttk.Entry(window, width=15, textvariable=record_num)
record_num.place(relx=.17, rely=.70,)

# The distance entry
distance_lbl = ttk.Label(window,
                         text="Record Distance",
                         font=("Helvetica", 12))
distance_lbl.place(relx=.28, rely=.70,)

distance = tk.StringVar()
distance = ttk.Entry(window, width=15, textvariable=distance)
distance.place(relx=.395, rely=.70,)

# The odometer entry
odometer_lbl = ttk.Label(window,
                         text="Odometer",
                         font=("Helvetica", 12))
odometer_lbl.place(relx=.51, rely=.70,)

odometer = tk.StringVar()
odometer = ttk.Entry(window, width=15, textvariable=odometer)
odometer.place(relx=.58, rely=.70,)

# The notes
notes_lbl = ttk.Label(window,
                      text="Notes:",
                      font=("Helvetica", 12))
notes_lbl.place(relx=.1, rely=.80,)

notes = tk.StringVar()
notes = ttk.Entry(window, width=90, textvariable=notes)
notes.place(relx=.17, rely=.80,)


def testing_complete():
    # ask are you sure

    MsgBox = messagebox.askquestion('Exit Application',
                                    'Are you sure you want to exit?',
                                    icon='warning',
                                    default='no')
    if MsgBox == 'yes':
        window.destroy()


# Record Record button
testing_complete = tk.Button(window,
                             text='Testing Complete',
                             command=testing_complete,
                             font=("Helvetica", 8))
testing_complete.place(relx=.9, rely=.90,)

window.mainloop()
