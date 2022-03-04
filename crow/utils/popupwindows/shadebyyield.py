import tkinter as tk


class shadebyyieldPopup(object):
    """
    Asks for which column to base the shading preference
    """

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="Column to base shading on:").place(x=0, y=0)
        self.shadecol = tk.Entry(top)
        self.shadecol.place(x=0, y=25)
        self.closebutton = tk.Button(top, text="Ok", command=self.close)
        self.closebutton.place(x=0, y=50)

    def close(self):
        self.shadecol = self.shadecol.get()
        self.top.destroy()
