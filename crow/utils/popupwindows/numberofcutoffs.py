import tkinter as tk


class numberofcutoffsPopup(object):
    """
    Asks user for both the column to base the groupign on and
    the number of groups to generate
    """

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="Number of groups:").place(x=0, y=0)
        self.numgroups = tk.Entry(top)
        self.numgroups.place(x=0, y=25)
        tk.Label(top, text="Column to base groups on:").place(x=0, y=50)
        self.cutoffcol = tk.Entry(top)
        self.cutoffcol.place(x=0, y=75)
        tk.Button(top, text="Ok", command=self.close).place(x=0, y=100)

    def close(self):
        self.numgroups = self.numgroups.get()
        self.cutoffcol = self.cutoffcol.get()
        self.top.destroy()
