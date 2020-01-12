#This is the wrapper function for Crow

#retrieve python packages that aren't built in for some stupid reason
import os
import tkinter as tk
from tkinter import ttk

#retrieve my functions written elsewhere
import ParseXML as ParseXML
from PrePull import PrePull
from Pull import Pull
from Present import Present
'''
#maww
def Crow():
    print("maww")
    return 0
'''
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
        #warning label
        self.warninglabel = tk.StringVar()
        tk.Label(master,textvariable=self.warninglabel, fg="#ff0000").place(x=0,rely=0.955)
        self.warninglabel.set("Warnings appear here!")
    #maww
    def call(self):
        #maww
        print("maww")
        #maww
    #maww

    
    #want to define a function that can be called from other classes to update the warning label
    def update_warning(self,newwarning):
        self.warninglabel.set(newwarning)
        
    #or just use tkinter to make a new error popup


