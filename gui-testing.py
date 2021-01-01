
# Import required modules
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import serial
import time

# Open Serial Port
serialPort = serial.Serial(port="COM30",
                           baudrate=9600,
                           bytesize=8,
                           timeout=2,
                           stopbits=serial.STOPBITS_ONE)
time.sleep(0.1)     # wait for pyserial port to actually be ready

# Global Varibles
Number_samples = 3
loop_count = 1
red_first_time = True
blue_first_time = True
green_first_time = True
red_recorded = False
blue_recorded = False
green_recorded = False

print('Blue Current Weight, Red Current Weight, Green Current Weight')
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


def Weight_read():

    serialString = ""  # Used to hold data coming over UART
    actual_weight = 0.00
    serialPort.flushInput()

    try:
        serialString = serialPort.readline()
        serialString = serialString.decode('Ascii').strip('+').strip()
        serialString = serialString[:-1]
        actual_weight = (float(serialString))

    except serial.SerialException:
        # There is no new data from serial port
        return(0)

    except ValueError:
        # just return 0 Zero if cant be converted to float, and try again
        return(0)

    except TypeError:
        # Disconnect of USB->UART occured
        # self.port.close()
        return(0)
    else:
        return(actual_weight)


def sample_weight():
    average_weight = []
    current_weight = 0.00

    for x in range(Number_samples):
        read = Weight_read()
        average_weight.append(read)

    current_weight = Weight_read()
    max_weight = max(average_weight)
    min_weight = min(average_weight)

    loop_count = 0
    try:
        while max_weight != min_weight or min_weight == 0:
            # reomve 1st entry
            average_weight.pop(0)
            # read scale
            current_weight = Weight_read()

            # add the current weight to end of list
            average_weight.append(current_weight)
            # find max and min desire them to be same
            max_weight = max(average_weight)
            min_weight = min(average_weight)
            loop_count += 1

            if loop_count > 25:
                print("this represents message box in Tkinter - check scale!")
                loop_count = 0

        return(current_weight)

    except TypeError:
        print('Check Scale - TypeError')
        pass


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
    global green_recorded
    global blue_recorded
    global red_recorded
    global loop_count  # TODO Loop_count needs to be distance and add odometer

    red_recorded = False
    blue_recorded = False
    green_recorded = False

    global blue_first_time
    global red_first_time
    global green_first_time

    # update the odometer
    total_odo = float(odo.get())
    dist_add = float(dist.get())
    total_odo = total_odo + dist_add
    odo.set("{:.4f}".format(total_odo))

    # Update the first time setup boolean
    blue_first_time = False
    red_first_time = False
    green_first_time = False

    BlueButton.config(text='Record', relief='raised')
    RedButton.config(text='Record', relief='raised')
    GreenButton.config(text='Record', relief='raised')

    # update record number
    record_num.set(loop_count)

    # compile brush data for CSV file
    green = ', '.join([str(elem) for elem in blue_brush])
    red = ', '.join([str(elem) for elem in red_brush])
    blue = ', '.join([str(elem) for elem in green_brush])
    notes_taken = notes.get()
    notes.set("")

    # Print to the terminal the current weight for each brush.
    screen_print = (str(blue_brush[5])
                    + ', '
                    + str(red_brush[5])
                    + ', '
                    + str(green_brush[5]))
    print(screen_print)

    record_data = (str(datetime.datetime.now())
                   + ", "
                   + str(loop_count)
                   + ", "
                   + green
                   + ", "
                   + red
                   + ", "
                   + blue
                   + ", "
                   + notes_taken)

    with open(filename, 'a') as f:
        loop_count += 1
        f.write(record_data)
        f.write('\n')
        f.close
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


# #############################################################################
#                                   Blue BUTTON
# #############################################################################

# Selected Red Brush
def Blue_clicked():
    global blue_first_time
    global blue_brush
    global blue_recorded

    # # Used for enter the record_complete() function.
    blue_recorded = True

    # Change button to be sunken.
    BlueButton.config(text='Recorded', relief='sunken')

    # Get the current weight from the scale
    current_weight = sample_weight()

    # Find out if this is the first record
    if blue_first_time:

        # Read the selected brush then make it grayed out
        brush_info = Blue_combo.get()
        Blue_combo.config(state="disabled")

        # [0] Item Number is a string 9 character from begining
        blue_brush[0] = brush_info[:9]

        # [2] Fiber Radius is 5 from end and a diameter
        blue_brush[2] = float(brush_info[-5:])/2

        # [3] Start length is in the middle of the string
        blue_brush[3] = float(brush_info[10:14].strip())

        # [1] Define fiber count
        blue_brush[1] = find_fiber_count(current_weight,
                                         blue_brush[2],
                                         blue_brush[3]
                                         )

        # [4]  Start weight put in entry and list
        blue_brush[4] = current_weight
        B_start.set(blue_brush[4])

        # [5]  Current weight
        blue_brush[5] = current_weight
        B_Current.set(blue_brush[5])

        # [6] Calculate difference from previous weight.
        blue_brush[6] = current_weight
        B_Previous.set(blue_brush[6])
        # Since this is the first weigh sample set differance to 0.
        B_diff.set(0.00)

        # [7] Current weight
        blue_brush[7] = blue_brush[3]
        B_est_length.set(blue_brush[7])

    else:
        # Update the previous widget.
        B_Previous.set(blue_brush[5])

        # [6] Update the difference list and text widget.
        sub = float(blue_brush[5]) - current_weight
        blue_brush[6] = "{:.1f}".format(sub)
        B_diff.set(blue_brush[6])

        # [5]  Update current weight widget.
        blue_brush[5] = current_weight
        B_Current.set(blue_brush[5])

        # [7] Update the current length widget.
        blue_brush[7] = "{:.4f}".format(find_height(current_weight,
                                                    blue_brush[2],
                                                    blue_brush[1]))

        B_est_length.set(blue_brush[7])

        # Have all colors been recorded
    if green_recorded and red_recorded and blue_recorded:
        record_complete()


BlueButton = tk.Button(window, text='Record', font=("Helvetica", 12),
                       command=Blue_clicked)
BlueButton.grid(column=2, row=50)


# #############################################################################
#                                   RED BUTTON
# #############################################################################

# Selected Red Brush
def Red_clicked():
    global red_first_time
    global red_brush
    global red_recorded

    # # Used for enter the record_complete() function.
    red_recorded = True

    # Change button to be sunken.
    RedButton.config(text='Recorded', relief='sunken')

    # Get the current weight from the scale
    current_weight = sample_weight()

    # Find out if this is the first record
    if red_first_time:

        # Read the selected brush then make it grayed out
        brush_info = Red_combo.get()
        Red_combo.config(state="disabled")

        # [0] Item Number is a string 9 character from begining
        red_brush[0] = brush_info[:9]

        # [2] Fiber Radius is 5 from end and a diameter
        red_brush[2] = float(brush_info[-5:])/2

        # [3] Start length is in the middle of the string
        red_brush[3] = float(brush_info[10:14].strip())

        # [1] Define fiber count
        red_brush[1] = find_fiber_count(current_weight,
                                        red_brush[2],
                                        red_brush[3]
                                        )

        # [4]  Start weight put in entry and list
        red_brush[4] = current_weight
        R_start.set(red_brush[4])

        # [5]  Current weight
        red_brush[5] = current_weight
        R_Current.set(red_brush[5])

        # [6] Calculate difference from previous weight.
        red_brush[6] = current_weight
        R_Previous.set(red_brush[6])
        # Since this is the first weigh sample set differance to 0.
        R_diff.set(0.00)

        # [7] Current weight
        red_brush[7] = red_brush[3]
        R_est_length.set(red_brush[7])

    else:
        # TODO remove this line - testing green_brush[7] is set in first_time
        red_brush[7] = 30.0

        # Update the previous widget.
        R_Previous.set(red_brush[5])

        # [6] Update the difference list and text widget.
        sub = float(red_brush[5]) - current_weight
        red_brush[6] = "{:.4f}".format(sub)
        R_diff.set(red_brush[6])

        # [5]  Update current weight widget.
        red_brush[5] = current_weight
        R_Current.set(red_brush[5])

        # [7] Update the current length widget.
        red_brush[7] = "{:.4f}".format(find_height(current_weight,
                                                   red_brush[2],
                                                   red_brush[1]))

        R_est_length.set(red_brush[7])

    # Have all colors been recorded
    if green_recorded and red_recorded and blue_recorded:
        record_complete()


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

    # Used for enter the record_complete() function.
    green_recorded = True

    # Change button to be sunken.
    GreenButton.config(text='Recorded', relief='sunken')

    # Get the current weight from the scale
    current_weight = sample_weight()

    # Find out if this is the first record, this code only executes
    # the first time, then all the rest is the else statment
    if green_first_time:

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

        # Since this is the first weigh sample set differance to 0.
        G_diff.set(0.00)

        # [7] Current Length
        green_brush[7] = green_brush[3]
        G_est_length.set(green_brush[7])

    else:
        # # TODO remove this line - testing green_brush[7] is set in first_time
        # green_brush[7] = 30.0

        # update the previous entry widget
        G_Previous.set(green_brush[5])

        # [6] update the difference list and text widget
        sub = float(green_brush[5]) - current_weight
        green_brush[6] = "{:.4f}".format(sub)
        G_diff.set(green_brush[6])

        # [5] Current weight
        green_brush[5] = current_weight
        G_Current.set(green_brush[5])

        # [7] update Current length

        green_brush[7] = "{:.4f}".format(find_height(current_weight,
                                                     green_brush[2],
                                                     green_brush[1]))

        G_est_length.set(green_brush[7])

    # Have all colors been recorded, if so complete record

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
Blue_start = ttk.Entry(window,
                       width=15,
                       textvariable=B_start,
                       state='readonly',
                       font=("Helvetica", 12),
                       justify='center'
                       )
Blue_start.grid(column=2, row=44)

Blue_Previous_lbl = ttk.Label(window,
                              text="Previous Weight(g)",
                              font=("Helvetica", 12))
Blue_Previous_lbl.grid(column=1, row=45,)

B_Previous = tk.StringVar()
Blue_Previous = ttk.Entry(window,
                          width=15,
                          textvariable=B_Previous,
                          state='readonly',
                          font=("Helvetica", 12),
                          justify='center'
                          )
Blue_Previous.grid(column=2, row=45)

Blue_Current_lbl = ttk.Label(window,
                             text="Current Weight(g)",
                             font=("Helvetica", 12))
Blue_Current_lbl.grid(column=1, row=46,)

B_Current = tk.StringVar()
Blue_Current = ttk.Entry(window,
                         width=15,
                         textvariable=B_Current,
                         state='readonly',
                         font=("Helvetica", 12),
                         justify='center'
                         )
Blue_Current.grid(column=2, row=46)

Blue_Diff_lbl = ttk.Label(window,
                          text="Difference Weight (g)",
                          font=("Helvetica", 12))
Blue_Diff_lbl.grid(column=1, row=47,)

B_diff = tk.StringVar()
Blue_diff = ttk.Entry(window,
                      width=15,
                      textvariable=B_diff,
                      state='readonly',
                      font=("Helvetica", 12),
                      justify='center'
                      )
Blue_diff.grid(column=2, row=47)

Blue_est_length_lbl = ttk.Label(window,
                                text="Est. Length (mm)",
                                font=("Helvetica", 12))
Blue_est_length_lbl.grid(column=1, row=48,)

B_est_length = tk.StringVar()
Blue_est_length = ttk.Entry(window,
                            width=15,
                            textvariable=B_est_length,
                            state='readonly',
                            font=("Helvetica", 12),
                            justify='center'
                            )
Blue_est_length.grid(column=2, row=48)

# Red labels and Text Boxes
Red_Start_lbl = ttk.Label(window,
                          text="Start Weight(g)",
                          font=("Helvetica", 12))
Red_Start_lbl.grid(column=6, row=44,)

R_start = tk.StringVar()
Red_start = ttk.Entry(window,
                      width=15,
                      textvariable=R_start,
                      state='readonly',
                      font=("Helvetica", 12),
                      justify='center'
                      )
Red_start.grid(column=7, row=44)

Red_Previous_lbl = ttk.Label(window,
                             text="Previous Weight(g)",
                             font=("Helvetica", 12))
Red_Previous_lbl.grid(column=6, row=45,)

R_Previous = tk.StringVar()
Red_Previous = ttk.Entry(window,
                         width=15,
                         textvariable=R_Previous,
                         state='readonly',
                         font=("Helvetica", 12),
                         justify='center'
                         )
Red_Previous.grid(column=7, row=45)

Red_Current_lbl = ttk.Label(window,
                            text="Current Weight(g)",
                            font=("Helvetica", 12))
Red_Current_lbl.grid(column=6, row=46,)

R_Current = tk.StringVar()
Red_Current = ttk.Entry(window,
                        width=15,
                        textvariable=R_Current,
                        state='readonly',
                        font=("Helvetica", 12),
                        justify='center'
                        )

Red_Current.grid(column=7, row=46)

Red_Diff_lbl = ttk.Label(window,
                         text="Difference Weight (g)",
                         font=("Helvetica", 12))
Red_Diff_lbl.grid(column=6, row=47,)

R_diff = tk.StringVar()
Red_diff = ttk.Entry(window,
                     width=15,
                     textvariable=R_diff,
                     state='readonly',
                     font=("Helvetica", 12),
                     justify='center'
                     )
Red_diff.grid(column=7, row=47)

Red_est_length_lbl = ttk.Label(window,
                               text="Est. Length (mm)",
                               font=("Helvetica", 12),
                               state='readonly',
                               justify='center'
                               )
Red_est_length_lbl.grid(column=6, row=48,)

R_est_length = tk.StringVar()
Red_est_length = ttk.Entry(window,
                           width=15,
                           textvariable=R_est_length,
                           state='readonly',
                           font=("Helvetica", 12),
                           justify='center'
                           )
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
record_num_entry = ttk.Entry(window, width=5,
                             textvariable=record_num,
                             state='readonly',
                             font=('Helvetica', 12),
                             justify='center'
                             )
record_num_entry.place(relx=.17, rely=.70,)

# The distance entry
distance_lbl = ttk.Label(window,
                         text="Record Distance",
                         font=("Helvetica", 12))
distance_lbl.place(relx=.28, rely=.70,)

dist = tk.DoubleVar(value=1.0)
distance = ttk.Spinbox(window,
                       textvariable=dist,
                       width=15,
                       from_=.1,
                       to=10,
                       increment=.1)
distance.place(relx=.395, rely=.70,)

# The odometer entry
odometer_lbl = ttk.Label(window,
                         text="Odometer",
                         font=("Helvetica", 12))
odometer_lbl.place(relx=.51, rely=.70,)

odo = tk.DoubleVar(0.00)
odometer = ttk.Entry(window,
                     width=15,
                     textvariable=odo,
                     state='readonly',
                     justify='center')
odometer.place(relx=.58, rely=.70,)

# The notes
notes_lbl = ttk.Label(window,
                      text="Notes:",
                      font=("Helvetica", 12))
notes_lbl.place(relx=.1, rely=.80,)

notes = tk.StringVar()
notes_entry = ttk.Entry(window,
                        width=90,
                        textvariable=notes,
                        )
notes_entry.place(relx=.17, rely=.80,)

given_filename = "filename: " + filename
filename_lbl = ttk.Label(window,
                         text=given_filename,
                         font=("Helvetica", 8)
                         )
filename_lbl.place(relx=.1, rely=.9)

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
