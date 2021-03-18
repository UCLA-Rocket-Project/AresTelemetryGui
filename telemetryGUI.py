from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import csv
import tkinter as tk
import matplotlib.pyplot as plt
import serial as sr
import numpy as np
import math
import pandas as pd

from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter

plt.style.use('seaborn')

# Global Variables
data = np.array([]) # empty array
t = np.array([])

plot_data_flag = False # Flag that tells gui when to be plotting data

startPoint = 0

# # Data (UNFINISHED)
def plot_data():
    global fieldnames, plot_data_flag, data, t, startPoint

    if (plot_data_flag):
        now_t = datetime.now()

        # Read in data from csv file
        if startPoint != 0:
            data = pd.read_csv('data.csv', skiprows = range(1,startPoint))
        else:
            data = pd.read_csv('data.csv')        

        # Appends current clock time to time array
        t = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')
        y1 = data['x_1']
        y2 = data['x_2']

        # Finds index of first element of time array with time delta less < 10 seconds (i.e. only the last 10 seconds of data will be plotted)
        for i in range(0,len(t)):
            temp_del = now_t-t[i]
            if temp_del > timedelta(seconds = 10):
                startPoint += i
            if temp_del < timedelta(seconds = 10):
                break

        lines.set_data(t, y1)
        lines2.set_data(t, y2)

        # Scale axes
        fig1.gca().relim()
        fig1.gca().set_xlim(now_t - timedelta(seconds = 10), now_t)
        fig1.gca().autoscale_view()

        fig2.gca().relim()
        fig2.gca().set_xlim(now_t - timedelta(seconds = 10), now_t)
        fig2.gca().autoscale_view()

        canvas.draw()
        canvas2.draw()

    root.after(1,plot_data)

# Start plotting data if not already plotting
def plot_start():
    global plot_data_flag, startPoint
    if ~plot_data_flag:
        plot_data_flag = True
        startPoint = 0
    # s.reset_input_buffer()

# Stop plotting data if data is being plotted
def plot_stop():
    global plot_data_flag
    if plot_data_flag:
        plot_data_flag = False

# Clear existing data
def plot_clear():
    global data, t
    data = np.array([])
    t = np.array([])

    lines.set_data(t, data)
    fig1.gca().relim()
    fig1.gca().autoscale_view()
    
    lines2.set_data(t, data)
    fig2.gca().relim()
    fig2.gca().autoscale_view()

    canvas.draw()
    canvas2.draw()

# GUI Main Code
root = tk.Tk() # Create tkinter object
root.title('Ares Telemetry GUI')
root.config(background = 'light blue') # Configure tkinter settings
root.geometry("1920x1080") # Set window resolution

# Plot figure 1 data to GUI
fig1 = Figure()
ax1 = fig1.add_subplot(111)

ax1.set_title('Test Plot')
ax1.set_xlabel('Test x')
ax1.set_ylabel('Test y')
ax1.xaxis.set_major_formatter(DateFormatter('%H:%M:%S')) 
ax1.fmt_xdata = DateFormatter('%H:%M:%S') 
fig1.autofmt_xdate() 
lines, = ax1.plot_date([],[],linestyle='solid',marker='o')

canvas = FigureCanvasTkAgg(fig1, master=root) # Create canvas figure object
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400) # Place figure at position (x,y) with size (width,height)
canvas.draw() # Draw the object

# Plot figure 2 data to GUI
fig2 = Figure()
ax2 = fig2.add_subplot(111)

ax2.set_title('Test Plot 2')
ax2.set_xlabel('Test x')
ax2.set_ylabel('Test y')
ax2.xaxis.set_major_formatter(DateFormatter('%H:%M:%S')) 
ax2.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S') 
fig2.autofmt_xdate() 
lines2, = ax2.plot_date([],[],linestyle='solid',marker='o')

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.get_tk_widget().place(x = 620, y = 10, width = 600, height = 400) # Place figure at position (x,y) with size (width,height)
canvas2.draw() # Draw the object

# Add buttons to interface
root.update(); # Update GUI
start = tk.Button(root, text = "Start Plot", font = ('calibri', 12), command = lambda: plot_start()) # Create button object that executes function plot_start()
start.place(x = 100, y = 750) # Place button at (x,y)

root.update()
stop = tk.Button(root, text = "Stop Plot", font = ('calibri', 12), command = lambda: plot_stop())
stop.place(x = start.winfo_x()+start.winfo_reqwidth() + 20, y = 750) # Place button right of start button

root.update()
clear = tk.Button(root, text = "Clear Plot", font = ('calibri', 12), command = lambda: plot_clear())
clear.place(x = stop.winfo_x()+stop.winfo_reqwidth() + 20, y = 750)

# Execute main GUI loop
root.after(1,plot_data)
root.mainloop()
