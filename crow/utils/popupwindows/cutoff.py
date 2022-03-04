import tkinter as tk


class cutoffPopup(object):
    """
    enable the user to make custom cutoff colors, useful for grouping wells
    by selectivity or yield
    """

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="For wells below this value:").place(x=0, y=0)
        self.cutoffval = tk.Entry(top)
        self.cutoffval.place(x=0, y=25)
        tk.Label(top, text="Use this color:").place(x=0, y=50)
        self.cutoffcolor = tk.Entry(top)
        self.cutoffcolor.insert(tk.END, "255,255,255")
        self.cutoffcolor.place(x=0, y=75)
        self.closebutton = tk.Button(top, text="Ok", command=self.close)
        self.closebutton.place(x=0, y=100)

    def close(self):
        self.cutoffval = self.cutoffval.get()
        self.cutoffcolor = self.cutoffcolor.get()
        self.top.destroy()
