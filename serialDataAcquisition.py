## MAKE SURE TO CLOSE ALL SERIAL CONNECTIONS FROM PI BEFORE RUNNING CODE

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import tkinter as tk
import matplotlib.pyplot as plt
import serial as sr
import numpy as np
import math
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter

plt.style.use('seaborn')

# Global Variables
data = np.array([]) # empty array
t = np.array([])

plot_data_flag = False

startTime = datetime.now()

# # Establish connection with Rasperry Pi over serial (UNFINISHED)
# s = sr.Serial('COM8',9600) # Connect to serial port COM8 with baudrate 9600
# s.reset_input_buffer() # Clear any data in buffer

# # Data (UNFINISHED)
def plot_data():
    global plot_data_flag, data, t, startTime

    if (plot_data_flag):
        # a = s.readline() # Read line from serial
        # a.decode()
        
        # For testing
        a = np.random.rand()

        data = np.append(data, a)

        t = np.append(t, datetime.now())

        lines.set_data(t, data)
        fig.gca().relim()
        fig.gca().autoscale_view()
        canvas.draw()

    root.after(1,plot_data)

def plot_start():
    global plot_data_flag, startTime
    plot_data_flag = True
    startTime = datetime.now()
    # s.reset_input_buffer()

def plot_stop():
    global plot_data_flag
    plot_data_flag = False

def plot_clear():
    global data, t
    data = np.array([])
    t = np.array([])
    lines.set_data(t, data)
    fig.gca().relim()
    fig.gca().autoscale_view()
    canvas.draw()

# GUI Main Code
root = tk.Tk() # Create tkinter object
root.title('Ares Telemetry GUI')
root.config(background = 'light blue') # Configure tkinter settings
root.geometry("1280x720") # Set window resolution

# Plot data to GUI
fig = Figure()
ax = fig.add_subplot(111)

ax.set_title('Test Plot')
ax.set_xlabel('Test x')
ax.set_ylabel('Test y')
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S')) 
ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S') 
fig.autofmt_xdate() 
lines, = ax.plot_date([],[])

canvas = FigureCanvasTkAgg(fig, master=root) # Create canvas figure object
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 450) # Place figure at position (x,y) with size (width,height)
canvas.draw() # Draw the object

# Add buttons to interface
root.update(); # Update GUI
start = tk.Button(root, text = "Start Plot", font = ('calibri', 12), command = lambda: plot_start()) # Create button object that executes function plot_start()
start.place(x = 100, y = 500) # Place button at (x,y)

root.update()
stop = tk.Button(root, text = "Stop Plot", font = ('calibri', 12), command = lambda: plot_stop())
stop.place(x = start.winfo_x()+start.winfo_reqwidth() + 20, y = 500) # Place button right of start button

root.update()
clear = tk.Button(root, text = "Clear Plot", font = ('calibri', 12), command = lambda: plot_clear())
clear.place(x = stop.winfo_x()+stop.winfo_reqwidth() + 20, y = 500)

root.after(1,plot_data)
root.mainloop()
