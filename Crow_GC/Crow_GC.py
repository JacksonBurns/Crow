# -*- coding: utf-8 -*-
# This is the wrapper function for Crow - GC
import glob
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plot
import traceback
from datetime import datetime
import tkinter.colorchooser as cc

# retrieve my functions written elsewhere
from helper_functions import ParseXML, RequestFiles

from Crow_GC import PrePull_GC as PrePull
from Crow_GC import Pull_GC as Pull
from Crow_GC import Present_GC as Present

# from PrePull_GC import PrePull
# from Pull_GC import Pull
# from Present_GC import Present

# retreive global datafiles list variable
from Crow_GC import globals_GC

globals_GC.init()


# define GUI
class Crow_GC(tk.Frame):
    def __init__(self, master):
        self.master = master
        master.title("Crow - GC")
        master.geometry("800x500")
        # set up 3 tabs
        tk.Frame.__init__(self)
        self.notebook = ttk.Notebook()
        self.notebook.add(PrePull.PrePull(self.notebook), text="Pre-Pull")
        self.notebook.add(Pull.Pull(self.notebook), text="Pull")
        self.notebook.add(Present.Present(self.notebook), text="Present")
        self.notebook.place(x=0, y=0)
        # add data selector
        self.FileDisplay = tk.StringVar()
        self.FileDisplay = ""
        # define select data callback function
        def selectrawdatacallback():
            globals_GC.datafiles = RequestFiles.RequestFiles(
                "Raw Data", "*.xml", globals_GC.rawdatapath
            )
            self.FileDisplay = (
                str(globals_GC.datafiles)
                .replace(",", "\n")
                .replace("(", "")
                .replace(")", "")
            )
            update_files()

        # define excel data callback
        def selectexceldatacallback():
            globals_GC.datafiles = RequestFiles.RequestFiles(
                "Processed Data", "*.csv", globals_GC.exportdatapath
            )
            self.FileDisplay = (
                str(globals_GC.datafiles)
                .replace(",", "\n")
                .replace("(", "")
                .replace(")", "")
            )
            update_files()

        # data files display
        def update_files():
            temp = tk.Text(master, height=10, width=35)
            temp.insert(
                tk.END,
                str(len(globals_GC.datafiles)) + " TOTAL FILES\n" + self.FileDisplay,
            )
            temp.place(x=470, y=65)
            temp.config(state="disabled")

        update_files()
        # data files label
        tk.Label(master, text="Current Data Files:").place(x=470, y=40)
        # Select Data files button
        tk.Button(master, text="Select Raw Data", command=selectrawdatacallback).place(
            x=470, y=245
        )
        # Select Data files button
        tk.Button(
            master, text="Select Excel Data", command=selectexceldatacallback
        ).place(x=650, y=245)

        # Retrieve files from server by experiment name
        def searchservercallback():
            globals_GC.datafiles = glob.glob(
                globals_GC.rawdatapath + "*" + self.expname.get() + "*"
            )
            self.FileDisplay = (
                str(globals_GC.datafiles)
                .replace(",", "\n")
                .replace("[", "")
                .replace("]", "")
            )
            update_files()

        tk.Button(
            master, text="Search Server by Expt. Name", command=searchservercallback
        ).place(x=470, y=310)
        self.expname = tk.Entry(master)
        self.expname.place(x=470, y=280)
        # title on top of window
        tk.Label(master, text="Crow Really Outta Work").place(relx=0.78, y=0)
        # setup callback for closing app
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)

    # apparently closing a window doesn't stop the main loop, what a great feature
    def close_app(self):
        if messagebox.askokcancel(title="Quit", message="Are you sure?"):
            plot.close("all")
            self.master.destroy()

    # maww
    def call(self):
        # maww
        print("maww")
        # maww

    # maww

