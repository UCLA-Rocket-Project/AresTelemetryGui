# ---------------------------------------------------------------------------#
# Import libraries
# ---------------------------------------------------------------------------#

import csv
import tkinter as tk
import matplotlib.pyplot as plt
import serial as sr
import numpy as np
import math
import pandas as pd

from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
from tkinter import *
from PIL import ImageTk, Image
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.animation import FuncAnimation

plt.style.use('seaborn')

# ---------------------------------------------------------------------------#
# Global variables
# ---------------------------------------------------------------------------#

data = np.array([]) # empty array
t = np.array([])
y1 = np.array([])
y2 = np.array([])

plot_data_flag = False # Flag that tells gui when to be plotting data

startPoint = 0


# ---------------------------------------------------------------------------#
# Pages
# ---------------------------------------------------------------------------#
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

#Page with charts
class chartsPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)    
        self.chartFrame = tk.Frame(self)
        self.chartFrame.pack(side="top", fill="x", expand=False)
        
        self.chart1Frame = tk.Frame(self.chartFrame)
        self.chart1Frame.pack(side="left",anchor=N, fill="x", expand=False)

        self.chart2Frame = tk.Frame(self.chartFrame)
        self.chart2Frame.pack(side="left",anchor=N, fill="x", expand=False)

        # Plot figure 1 data to GUI
        self.fig1 = Figure()
        self.ax1 = self.fig1.add_subplot(111)

        self.ax1.set_title('Test Plot')
        self.ax1.set_xlabel('Test x')
        self.ax1.set_ylabel('Test y')
        self.ax1.xaxis.set_major_formatter(DateFormatter('%H:%M:%S')) 
        self.ax1.fmt_xdata = DateFormatter('%H:%M:%S') 
        self.fig1.autofmt_xdate() 
        self.lines, = self.ax1.plot_date([],[],linestyle='solid',marker='o')

        self.canvas = FigureCanvasTkAgg(self.fig1, master=self.chart1Frame) # Create canvas figure object
        self.canvas.get_tk_widget().pack(side="top",anchor=W) # Place figure at position (x,y) with size (width,height)
        self.canvas.draw() # Draw the object

        # Plot figure 2 data to GUI
        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot(111)

        self.ax2.set_title('Test Plot 2')
        self.ax2.set_xlabel('Test x')
        self.ax2.set_ylabel('Test y')
        self.ax2.xaxis.set_major_formatter(DateFormatter('%H:%M:%S')) 
        self.ax2.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S') 
        self.fig2.autofmt_xdate() 
        self.lines2, = self.ax2.plot_date([],[],linestyle='solid',marker='o')

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.chart2Frame)
        self.canvas2.get_tk_widget().pack(side="top",anchor=W) # Place figure at position (x,y) with size (width,height)
        self.canvas2.draw() # Draw the object

        # self.toolbarFrame = tk.Frame(self)
        # self.toolbarFrame.pack(side="top", fill="x", expand=False)

        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.chart1Frame)
        self.toolbar1.update()
        self.toolbar1.pack(side="top",anchor=W,fill='x')

        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.chart2Frame)
        self.toolbar2.update()
        self.toolbar2.pack(side="top",anchor=W,fill='x')

        self.chartButtonframe = tk.Frame(self)
        self.chartButtonframe.pack(side="top", fill="x", expand=False)
        
        self.start = tk.Button(self.chartButtonframe, text = "Start Plot", font = ('calibri', 12), command = lambda: self.plot_start()) # Create button object that executes function plot_start()
        self.start.pack(side="left",fill='x',expand=True,anchor=N)
        self.stop = tk.Button(self.chartButtonframe, text = "Stop Plot", font = ('calibri', 12), command = lambda: self.plot_stop())
        self.stop.pack(side="left",fill='x',expand=True,anchor=N)
        self.clear = tk.Button(self.chartButtonframe, text = "Clear Plot", font = ('calibri', 12), command = lambda: self.plot_clear())
        self.clear.pack(side="left",fill='x',expand=True,anchor=N)

    def plot_data(self):
        global fieldnames, plot_data_flag, data, t, y1, y2, startPoint

        if (plot_data_flag):
            now_t = datetime.now()

            # Read in data from csv file
            try:
                if startPoint != 0:
                    data = pd.read_csv('data.csv', skiprows = range(1,startPoint))
                else:
                    data = pd.read_csv('data.csv')      
            except:
                plot_data_flag = False
                print("No data availiable to plot")
                return

            # Appends current clock time to time array
            t = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')
            y1 = data['x_1']
            y2 = data['x_2']

            # Finds index of first element of time array with time delta less < 10 seconds (i.e. only the last 10 seconds of data will be plotted)
            for i in range(0,len(t)):
                temp_del = now_t-t[i]
                if temp_del < timedelta(seconds = 10):
                    startPoint += i
                    break

            self.lines.set_data(t, y1)
            self.lines2.set_data(t, y2)

            # Scale axes
            self.fig1.gca().relim()
            self.fig1.gca().set_xlim(now_t - timedelta(seconds = 10), now_t)
            self.fig1.gca().autoscale_view()

            self.fig2.gca().relim()
            self.fig2.gca().set_xlim(now_t - timedelta(seconds = 10), now_t)
            self.fig2.gca().autoscale_view()

            self.canvas.draw()
            self.canvas2.draw()

    # Start plotting data if not already plotting
    def plot_start(self):
        global plot_data_flag, startPoint
        if ~plot_data_flag:
            plot_data_flag = True

    # Stop plotting data if data is being plotted
    def plot_stop(self):
        global plot_data_flag
        if plot_data_flag:
            plot_data_flag = False

    # Clear existing data
    def plot_clear(self):
        global data, t
        data = np.array([])
        t = np.array([])

        self.lines.set_data(t, data)
        self.fig1.gca().relim()
        self.fig1.gca().autoscale_view()
        
        self.lines2.set_data(t, data)
        self.fig2.gca().relim()
        self.fig2.gca().autoscale_view()

        self.canvas.draw()
        self.canvas2.draw()

#Info Page
class infoPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.charts = chartsPage(self)
        info = infoPage(self)

        buttonframe = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        #placing charts page
        self.charts.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        info.place(in_=container, x=0, y=0, relwidth=1, relheight=1)  

        #charts button
        self.chartsImageObj = Image.open("./pics/charts.png")
        self.chartsImage = ImageTk.PhotoImage(self.chartsImageObj)
        chartsButton = tk.Button(buttonframe, image=self.chartsImage,
            text="Charts", command=self.charts.lift)        

        self.infoImageObj = Image.open("./pics/help.png")
        self.infoImage = ImageTk.PhotoImage(self.infoImageObj)
        infoButton = tk.Button(buttonframe, image=self.infoImage,
            text="Info", command=info.lift)

        chartsButton.pack(side="left", fill="both",expand=True)
        infoButton.pack(side="left",fill="both",expand=True)

        self.charts.show()
        self.fEmbeddedCall()

    def fEmbeddedCall(self):
        self.charts.plot_data()
        self.after(1,self.fEmbeddedCall)

# ---------------------------------------------------------------------------#
# Initialization of GUI and plots
# ---------------------------------------------------------------------------#
if __name__ == "__main__":
    # GUI Main Code
    root = tk.Tk() # Create tkinter object
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title('Ares Telemetry GUI')
    root.config(background = 'light blue') # Configure tkinter settings
    root.geometry("1920x1080") # Set window resolution

    root.mainloop()
