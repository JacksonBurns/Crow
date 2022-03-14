import tkinter as tk


class shadebyyieldPopup(object):
    """GUI popup to ask for which column to base the shading.

    Args:
        object (tk.Top): Base window over which to draw this pop-up.
    """

    def __init__(self, master):
        """Constructor for GUI.

        Args:
            master (tk.Tk): tkinter UI window.
        """
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="Column to base shading on:").place(x=0, y=0)
        self.shadecol = tk.Entry(top)
        self.shadecol.place(x=0, y=25)
        self.closebutton = tk.Button(top, text="Ok", command=self.close)
        self.closebutton.place(x=0, y=50)

    def close(self):
        """Pack value into an attribute and then destroy the window.
        """
        self.shadecol = self.shadecol.get()
        self.top.destroy()
