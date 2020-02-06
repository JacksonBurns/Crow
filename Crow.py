'''#!/usr/bin/python3.6
# -*- coding: utf-8 -*-'''
"""
Created on Sat Jan 18 23:45:07 2020

@author: jackson
"""
#parent gui for all Crow family apps
from PIL import Image, ImageTk
import tkinter as tk
import Crow_GC

def startrek3():
    spock = tk.Tk()
    spock.title("Crow")
    spock.geometry("250x110")

    def Crow_GCcallback():
        startrek2(spock)
        root=tk.Tk()
        Crow_GC.Crow_GC(root)
        root.mainloop()
        startrek3()
        
    GCButton = tk.Button(spock, text ="GC", command = Crow_GCcallback)
    GCButton.place(x=10,y=10)

    def Crow_LCMScallback():
        '''
        startrek2(spock)
        root=tk.Tk()
        Crow_LCMS.Crow_LCMS(root)
        root.mainloop()
        startrek3()
        '''
        tk.messagebox.showinfo(message="Work in progress.")
        
    LCMSButton = tk.Button(spock, text ="LC/MS", command = Crow_LCMScallback, state=tk.DISABLED)
    LCMSButton.place(x=10,y=40)

    def Crow_SFCMScallback():
        '''
        startrek2(spock)
        root=tk.Tk()
        Crow_SFCMS.Crow_SFCMS(root)
        root.mainloop()
        startrek3()
        '''
        tk.messagebox.showinfo(message="Work in progress.")
        
    SFCMSButton = tk.Button(spock, text ="SFC/MS", command = Crow_SFCMScallback, state=tk.DISABLED)
    SFCMSButton.place(x=10,y=70)
    
    load = Image.open("Crow_logo.png")
    load = load.resize((160,160), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render)
    img.image = render
    img.place(x=90,y=-15)
    spock.mainloop()
    
def startrek2(spock):
    '''KHAN!'''
    spock.destroy()
    
startrek3()