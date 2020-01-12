import tkinter as tk
import Crow as C
class PrePull(tk.Frame):
    def __init__(self,name):
        tk.Frame.__init__(self,width=797,height=450)
        #define pre-pull callback function
        def prepullcallback():
            print("spaghetti foo")

        #Pre-Pull button
        tk.Button(self,text="Pre-Pull",command=prepullcallback).place(x=80,y=80)