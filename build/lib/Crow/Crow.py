from PIL import Image, ImageTk
import tkinter as tk
from Crow_GC import Crow_GC

"""
Created on Sat Jan 18 23:45:07 2020

Parent GUI for all Crow apps

@author: jackson
"""


def Crow_Parent():
    # Open a new tk window and name it
    window = tk.Tk()
    window.title("Crow")
    window.geometry("250x110")

    def Crow_GCcallback():
        """
        Close existing window, create a new root and instantiate GC app,
        upon exiting the GC app re-instantiates Parent app
        """
        Close_tk(window)
        root = tk.Tk()
        Crow_GC.Crow_GC(root)
        root.mainloop()
        Crow_Parent()

    GCButton = tk.Button(window, text="GC", command=Crow_GCcallback)
    GCButton.place(x=10, y=10)

    def Crow_LCMScallback():
        """
        Close existing window, create a new root and instantiate LC/MS app,
        upon exiting the LC/MS app re-instantiates Parent app
        """
        """
        Close_tk(window)
        root=tk.Tk()
        Crow_LCMS.Crow_LCMS(root)
        root.mainloop()
        Crow_Parent()
        """
        tk.messagebox.showinfo(message="Work in progress.")

    LCMSButton = tk.Button(
        window, text="LC/MS", command=Crow_LCMScallback, state=tk.DISABLED
    )
    LCMSButton.place(x=10, y=40)

    def Crow_SFCMScallback():
        """
        Close existing window, create a new root and instantiate SFC/MS app,
        upon exiting the SFC/MS app re-instantiates Parent app
        """
        """
        Close_tk(window)
        root=tk.Tk()
        Crow_SFCMS.Crow_SFCMS(root)
        root.mainloop()
        Crow_Parent()
        """
        tk.messagebox.showinfo(message="Work in progress.")

    SFCMSButton = tk.Button(
        window, text="SFC/MS", command=Crow_SFCMScallback, state=tk.DISABLED
    )
    SFCMSButton.place(x=10, y=70)

    # add Crow logo to parent application
    load = Image.open("./other/Crow_logo.png")
    load = load.resize((160, 160), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render)
    img.image = render
    img.place(x=90, y=-15)
    # start the app
    window.mainloop()


def Close_tk(inWindow):
    """
    Close window in order to resintate tk root window and pass to next App
    """
    inWindow.destroy()


Crow_Parent()
