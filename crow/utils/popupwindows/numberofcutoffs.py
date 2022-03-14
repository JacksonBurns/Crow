import tkinter as tk


class numberofcutoffsPopup(object):
    """
    Asks user for both the column to base the grouping on and
    the number of groups to generate.

    Args:
        object (tk.Top): Base window over which to draw this pop-up.
    """

    def __init__(self, master):
        """Constructor for GUI.

        Args:
            master (tk.Tk): tkinter UI window.
        """
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="Number of groups:").place(x=0, y=0)
        self.numgroups = tk.Entry(top)
        self.numgroups.place(x=0, y=25)
        tk.Label(top, text="Column to base groups on:").place(x=0, y=50)
        self.cutoffcol = tk.Entry(top)
        self.cutoffcol.place(x=0, y=75)
        self.closebutton = tk.Button(top, text="Ok", command=self.close)
        self.closebutton.place(x=0, y=100)

    def close(self):
        """Pack values into attributes and then destroy the window.
        """
        self.numgroups = self.numgroups.get()
        self.cutoffcol = self.cutoffcol.get()
        self.top.destroy()
