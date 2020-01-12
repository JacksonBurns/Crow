#This is the wrapper function for Crow

#retrieve python packages that aren't built in for some stupid reason
import os
import tkinter as tk
from tkinter import ttk, messagebox

#retrieve my functions written elsewhere
import ParseXML as ParseXML
import RequestFiles as RequestFiles
from PrePull import PrePull
from Pull import Pull
from Present import Present

#define GUI
class Crow(tk.Frame):
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
        
        #title on top of window
        tk.Label(master, text="Crow Really Outta Work").place(relx=0.405,y=0)

        #setup callback for closing app
        self.master.protocol('WM_DELETE_WINDOW', self.close_app)
        
    #apparently closing a window doesn't stop the main loop, what a great feature
    def close_app(self):
        if messagebox.askokcancel(title="Quit Crow",message="Are you sure?"):
            self.master.destroy()
    #maww
    def call(self):
        #maww
        print("maww")
        #maww
    #maww