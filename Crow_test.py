#!/usr/bin/python3.6
import Crow_GC as Crow
import time
#C.Crow()


import tkinter
root = tkinter.Tk()
my_gui = Crow.Crow_GC(root)
my_gui.call()
root.mainloop()
try:
    root.destroy()
    my_gui.destroy()
except:
    pass