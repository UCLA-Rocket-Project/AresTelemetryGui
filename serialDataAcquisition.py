## MAKE SURE TO CLOSE ALL SERIAL CONNECTIONS FROM PI BEFORE RUNNING CODE

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

filename = datetime.now().strftime("%d-%m-%Y_(%H;%M;%S)")+'.csv'

plot_data_flag = False # Flag that tells gui when to be plotting data

zeroT = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) # Used in calculation of relative time

fieldnames = ["time", "data"]

# # Data (UNFINISHED)
def plot_data():
    global fieldnames, plot_data_flag, data, t, startTime, zeroT

    if (plot_data_flag):
        startPoint = 0 # index of when to start plotting data

        # For testing without rasperry pi generate random value
        a = np.random.rand()

        # get time that data was obtained
        now_t = datetime.now()
        
        with open(filename, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)

            info = {

                "time": now_t,
                "data": a
            }

            csv_writer.writerow(info)

        # Append value to data array (add more data arrays as needed in the case of other measurements)
        data = np.append(data, a)

        # Appends current clock time to time array
        t = np.append(t, now_t)

        # Finds index of first element of time array with time delta less < 10 seconds (i.e. only the last 10 seconds of data will be plotted)
        for i in range(startPoint,len(t)):
            temp_del = now_t-t[i]
            if temp_del > timedelta(seconds = 10):
                startPoint = i
            if temp_del < timedelta(seconds = 10):
                break

        endPoint = len(t)-1

        if startPoint < 0:
            startPoint = 0
        if endPoint < 0:
            endPoint = 0

        t = t[startPoint:endPoint+1]
        data = data[startPoint:endPoint+1]

        lines.set_data(t, data)
        lines2.set_data(t, data*-10)

        endPoint = len(t)-1

        if startPoint < 0:
            startPoint = 0
        if endPoint < 0:
            endPoint = 0

        # Scale axes
        fig1.gca().relim()
        fig1.gca().set_xlim(t[endPoint] - timedelta(seconds = 10), t[endPoint])
        fig1.gca().autoscale_view()

        fig2.gca().relim()
        fig2.gca().set_xlim(t[endPoint] - timedelta(seconds = 10), t[endPoint])
        fig2.gca().autoscale_view()


        canvas.draw()
        canvas2.draw()

    root.after(1,plot_data)

# Start plotting data if not already plotting
def plot_start():
    global plot_data_flag, startTime
    if ~plot_data_flag:
        plot_data_flag = True
        startTime = datetime.now()
    # s.reset_input_buffer()

# Stop plotting data if data is being plotted
def plot_stop():
    global plot_data_flag
    if plot_data_flag:
        plot_data_flag = False

# Clear existing data
def plot_clear():
    global data, t, startPoint
    data = np.array([])
    t = np.array([])
    startPoint = 0
    lines.set_data(t, data)
    fig1.gca().relim()
    fig1.gca().autoscale_view()
    
    lines2.set_data(t, data)
    fig2.gca().relim()
    fig2.gca().autoscale_view()

    canvas.draw()
    canvas2.draw()

# Export data to excel sheet
def export_data():
    global data, t, rel_t_array, plot_data_flag
    if plot_data_flag:
        plot_data_flag = False
    df = pd.DataFrame.from_dict({'Time':t,'Relative Time':rel_t_array,'Data':data})
    df.to_excel(datetime.now().strftime("%d-%m-%Y_(%H;%M;%S)")+'.xlsx', header=True, index=False)
    print("Data Exported to test.xlsx")

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
lines, = ax1.plot_date([],[])

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
lines2, = ax2.plot_date([],[])

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

root.update()
export = tk.Button(root, text = "Stop and Export Data", font = ('calibri', 12), command = lambda: export_data())
export.place(x = clear.winfo_x()+stop.winfo_reqwidth() + 20, y = 750)


with open(filename, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# Execute main GUI loop
root.after(1,plot_data)
root.mainloop()
