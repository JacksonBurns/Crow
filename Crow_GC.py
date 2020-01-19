# -*- coding: utf-8 -*-

#This is the wrapper function for Crow - GC

#retrieve python packages that aren't built in for some stupid reason
import glob
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

#retrieve my functions written elsewhere
import ParseXML as ParseXML
import RequestFiles as RequestFiles
from PrePull_GC import PrePull
from Pull_GC import Pull
from Present_GC import Present

#retreive global datafiles list variable
import globals_GC as globals
globals.init()

#define GUI
class Crow_GC(tk.Frame):
    def __init__(self, master):
        #idk what this does really
        self.master = master
        master.title("Crow - GC")
        master.geometry("800x500")
        
        #set up 3 tabs
        tk.Frame.__init__(self)
        self.notebook = ttk.Notebook()
        self.notebook.add(PrePull(self.notebook),text="Pre-Pull")
        self.notebook.add(Pull(self.notebook),text="Pull")
        self.notebook.add(Present(self.notebook),text="Present")
        self.notebook.place(x=0,y=0)
        
        #add data selector
        ###self.datafiles = []
        self.FileDisplay = tk.StringVar()
        self.FileDisplay = ""
        #define select data callback function
        def selectrawdatacallback():
            globals.datafiles = RequestFiles.RequestFiles("Raw Data","*.xml")
            self.FileDisplay = str(globals.datafiles).replace(",","\n").replace("(","").replace(")","")
            update_files()
        #define excel data callback
        def selectexceldatacallback():
            globals.datafiles = RequestFiles.RequestFiles("Processed Data","*.csv")
            self.FileDisplay = str(globals.datafiles).replace(",","\n").replace("(","").replace(")","")
            update_files()
        #data files display
        def update_files():
            temp = tk.Text(master,height=10,width=40)
            temp.insert(tk.END,str(len(globals.datafiles))+" TOTAL FILES\n"+self.FileDisplay)
            temp.place(x=470,y=65)
            temp.config(state="disabled")
        update_files()
        #data files label
        tk.Label(master,text="Current Data Files:").place(x=470,y=40)
        #Select Data files button
        tk.Button(master,text="Select Raw Data",command=selectrawdatacallback).place(x=470,y=245)
        #Select Data files button
        tk.Button(master,text="Select Excel Data",command=selectexceldatacallback).place(x=650,y=245)
        #Retrieve files from server by experiment name
        def searchservercallback():
            ##########     MAKE THIS THE SERVER ADDRESS     ###########
            globals.datafiles = glob.glob("/home/jackson/Desktop/SampleData/*"+self.expname.get()+"*")
            self.FileDisplay = str(globals.datafiles).replace(",","\n").replace("[","").replace("]","")
            update_files()
        tk.Button(master,text="Search Server by Expt. Name",command=searchservercallback).place(x=470,y=310)
        self.expname = tk.Entry(master)
        self.expname.place(x=470,y=280)
        
        
        #title on top of window
        tk.Label(master, text="Crow Really Outta Work").place(relx=0.78,y=0)

        #setup callback for closing app
        self.master.protocol('WM_DELETE_WINDOW', self.close_app)
        
    #apparently closing a window doesn't stop the main loop, what a great feature
    def close_app(self):
        if messagebox.askokcancel(title="Quit",message="Are you sure?"):
            self.master.destroy()
            '''Crow.revivespock()'''
        
    #maww
    def call(self):
        #maww
        print("maww")
        #maww
    #maww