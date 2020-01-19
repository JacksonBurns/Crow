#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:45:07 2020

@author: jackson
"""

#parent gui for all Crow family apps

import tkinter as tk
import Crow_GC

def revivespock():
    spock = tk.Tk()

    def Crow_GCcallback():
        spock.destroy()
        root=tk.Tk()
        my_gui = Crow_GC.Crow_GC(root)
        my_gui.call()
        root.mainloop()
        revivespock()
    GCButton = tk.Button(spock, text ="GC", command = Crow_GCcallback)
    GCButton.place(x=0,y=0)

    def Crow_LCMScallback():
        '''
        spock.destroy()
        root=tk.Tk()
        my_gui = Crow_LCMS.Crow_LCMS(root)
        my_gui.call()
        root.mainloop()
        revivespock()
        '''
        tk.messagebox.showinfo(message="Oops... doesn't exist yet.")
        
    LCMSButton = tk.Button(spock, text ="LCMS", command = Crow_LCMScallback)
    LCMSButton.place(x=0,y=20)

    spock.mainloop()
    
revivespock()