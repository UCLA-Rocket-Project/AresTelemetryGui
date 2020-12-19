## MAKE SURE TO CLOSE ALL SERIAL CONNECTIONS FROM PI BEFORE RUNNING CODE

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import tkinter as tk
import matplotlib.pyplot as plt
import serial as sr
import numpy as np
import math
import time

# Global Variables
data = np.array([]) # empty array

plot_data_flag = False

# # Establish connection with Rasperry Pi over serial (UNFINISHED)
# s = sr.Serial('COM8',9600) # Connect to serial port COM8 with baudrate 9600
# s.reset_input_buffer() # Clear any data in buffer

# # Data (UNFINISHED)
# def plot_data():
#     global plot_data_flag, data

#     if (plot_data_flag):
#         a = s.readline() # Read line from serial
#         a.decode()

#         # Only plot 100 data elements at a time. I copied this from the tutorial, but I might change it so that the x axis moves with time
#         if(len(data) < 100):
#             data = np.append(data,float(a[0:4]))
#         else:
#             data[0:99] = data[1:100] # Shift data plot to left
#             data[99] = float(a[0:4]) # Current data value

#         lines.set_xdata(np.arange(0,len(data)))
#         lines.set_ydata(data)

#         canvas.draw()

#     root.after(1,plot_data)

def plot_start()
    global plot_data_flag
    plot_data_flag = True
    s.reset_input_buffer()

def plot_stop()
    global plot_data_flag
    plot_data_flag = False

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
ax.set_xlim(0,100)
ax.set_ylim(0,10)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root) # Create canvas figure object
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 450) # Place figure at position (x,y) with size (width,height)
canvas.draw() # Draw the object

# Add buttons to interface
root.update(); # Update GUI
start = tk.Button(root, text = "Start Plot", font = ('calibri', 12), command = lambda: plot_start()) # Create button object that executes function plot_start()
start.place(x = 100, y = 500) # Place button at (x,y)

root.update()
stop = tk.Button(root, text = "Stop Plot", font = ('calibri', 12), command = lambda: plot_stop())
stop.place(x = start.winfo_x()+start.winfo_reqwidth() + 20, y = 450) # Place button right of start button

root.after(1,plot_data)
root.mainloop()
