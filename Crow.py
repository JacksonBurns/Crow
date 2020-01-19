#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:45:07 2020

@author: jackson
"""

#parent gui for all Crow family apps
from PIL import Image, ImageTk
import tkinter as tk
import Crow_GC

def revivespock():
    spock = tk.Tk()
    spock.title("Crow Launcher")
    spock.geometry("300x110")

    def Crow_GCcallback():
        spock.destroy()
        root=tk.Tk()
        Crow_GC.Crow_GC(root)
        root.mainloop()
        revivespock()
    GCButton = tk.Button(spock, text ="GC", command = Crow_GCcallback)
    GCButton.place(x=10,y=10)

    def Crow_LCMScallback():
        '''
        spock.destroy()
        root=tk.Tk()
        Crow_LCMS.Crow_LCMS(root)
        root.mainloop()
        revivespock()
        '''
        tk.messagebox.showinfo(message="Oops... doesn't exist yet.")
        
    LCMSButton = tk.Button(spock, text ="LC/MS", command = Crow_LCMScallback)
    LCMSButton.place(x=10,y=40)

    def Crow_SFCMScallback():
        '''
        spock.destroy()
        root=tk.Tk()
        Crow_SFCMS.Crow_SFCMS(root)
        root.mainloop()
        revivespock()
        '''
        tk.messagebox.showinfo(message="Oops... doesn't exist yet.")
        
    SFCMSButton = tk.Button(spock, text ="SFC/MS", command = Crow_SFCMScallback)
    SFCMSButton.place(x=10,y=70)
    
    load = Image.open("temp_logo.png")
    load = load.resize((90,90), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render)
    img.image = render
    img.place(x=150, y=10)
    
    spock.mainloop()
    
revivespock()