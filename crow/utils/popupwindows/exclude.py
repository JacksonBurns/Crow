import tkinter as tk


class excludePopup(object):
    """
    Pop up which will ask the user which column they want to check
    and the value floor, for which wells below will not be displayed.

    Ex. Creating a selectivity chart, but not displaying wells where the
    yield is vanishingly small.
    """

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="Column to filter by:").place(x=0, y=0)
        self.excludecol = tk.Entry(top)
        self.excludecol.place(x=0, y=25)
        tk.Label(top, text="Hide wells with values below:").place(x=0, y=50)
        self.excludeval = tk.Entry(top)
        self.excludeval.place(x=0, y=75)
        self.closebutton = tk.Button(top, text="Ok", command=self.close)
        self.closebutton.place(x=0, y=100)

    def close(self):
        self.excludecol = self.excludecol.get()
        self.excludeval = self.excludeval.get()
        self.top.destroy()
