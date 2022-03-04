from PIL import Image, ImageTk
import tkinter as tk
import pkg_resources
import webbrowser
import pkg_resources
import sys
import glob
import tkinter as tk
from tkinter import ttk, messagebox
from crow.uitabs.PrePull import PrePull
from crow.uitabs.Pull import Pull
from crow.uitabs.Present import Present
from crow.utils import RequestFiles
from crow.utils.crow_globals import crow_globals

# initialize the global variables
crow_globals = crow_globals()


"""
Created on Sat Jan 18 23:45:07 2020

Parent GUI for all Crow apps

@author: jackson
"""


class CrowBase(tk.Frame):
    """
    Parent window for the GC app, which contains the global variables
    including raw data and input data, as well as holding the notebook
    which containts the 3 tabs (PrePull, Pull, Present)

    """

    def __init__(self, master):
        # crow_globals.init()
        # create base window, name it, and size it
        self.master = master
        master.title("Crow")
        master.geometry("800x500")
        # set up 3 tabs
        tk.Frame.__init__(self)
        self.notebook = ttk.Notebook()
        self.notebook.add(
            PrePull(self.notebook, crow_globals),
            text="Pre-Pull",
        )
        self.notebook.add(
            Pull(self.notebook, crow_globals),
            text="Pull",
        )
        self.notebook.add(
            Present(self.notebook, crow_globals),
            text="Present",
        )
        self.notebook.place(x=0, y=0)
        # add data selector
        self.FileDisplay = tk.StringVar()
        self.FileDisplay = ""

        # add Crow logo to base window
        resource_path = pkg_resources.resource_filename(
            __name__, "Crow_logo.png")
        load = Image.open(resource_path)
        load = load.resize((160, 160), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(image=render)
        img.image = render
        img.place(x=640, y=370)

        # define select data callback function
        def selectrawdatacallback():
            """
            Upon clicking the select data button, open up a file request window
            and set the currently selected files to those which are selected,
            update the display
            """
            crow_globals.datafiles = RequestFiles.RequestFiles(
                "Raw Data", "*.xml", crow_globals.rawdatapath
            )
            self.FileDisplay = (
                str(crow_globals.datafiles)
                .replace(",", "\n")
                .replace("(", "")
                .replace(")", "")
            )
            update_files()
            pass

        # define excel data callback
        def selectexceldatacallback():
            """
            Create pop-up file request for ".csv" input data for present
            """
            crow_globals.datafiles = RequestFiles.RequestFiles(
                "Processed Data", "*.csv", crow_globals.exportdatapath
            )
            self.FileDisplay = (
                str(crow_globals.datafiles)
                .replace(",", "\n")
                .replace("(", "")
                .replace(")", "")
            )
            update_files()
            pass

        # data files display
        def update_files():
            """
            Counts the total number of files selected (useful for large experiments)
            and concatenates to the beggining of the list of file names.
            """
            temp = tk.Text(master, height=10, width=35)
            temp.insert(
                tk.END,
                str(len(crow_globals.datafiles)) +
                " TOTAL FILES\n" + self.FileDisplay,
            )
            temp.place(x=470, y=65)
            temp.config(state="disabled")
            pass

        update_files()
        # data files label
        tk.Label(master, text="Current Data Files:").place(x=470, y=40)
        # Select Data files button
        tk.Button(master, text="Select Raw Data", command=selectrawdatacallback).place(
            x=470, y=245
        )
        # Select Data files button
        tk.Button(
            master, text="Select Processed Data (.csv)", command=selectexceldatacallback
        ).place(x=600, y=245)

        # Retrieve files from server by experiment name
        def searchservercallback():
            """
            Go to given 'server' location and glob for any file matching
            the given experiment name
            """
            crow_globals.datafiles = glob.glob(
                crow_globals.rawdatapath + "*" + self.expname.get() + "*"
            )
            self.FileDisplay = (
                str(crow_globals.datafiles)
                .replace(",", "\n")
                .replace("[", "")
                .replace("]", "")
            )
            update_files()
            pass

        def openconfigcallback():
            webbrowser.open(pkg_resources.resource_filename(
                __name__, "utils/config.yaml"))

        tk.Button(master, text="Open Config. File", command=openconfigcallback).place(
            x=470, y=340
        )

        tk.Button(
            master, text="Search Server by Expt. Name", command=searchservercallback
        ).place(x=470, y=310)
        self.expname = tk.Entry(master)
        self.expname.place(x=470, y=280)
        # title on top of window
        tk.Label(master, text="Crow Really Outta Work").place(relx=0.78, y=0)
        # setup callback for closing app
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)

    def close_app(self):
        """
        Adds a pop-up message to ensure that the user actually intended to quit,
        then on confirmation destorys the app so that the parent GUI
        can be launched again.
        """
        if messagebox.askokcancel(title="Quit", message="Are you sure?"):
            sys.exit(0)


# Helpful method for PyPi package console script entry point
def main():
    # Print a greeting
    print('''
    Thank you for installing Crow!
    Please visit the GitHub page for help with running Crow: https://github.com/JacksonBurns/Crow

    If you use Crow in published work, please cite this publication:
    https://figshare.com/articles/software/Crow_-_High_Throughput_Experimentation_Data_Retrieval_and_Presentation_GUI/11741898
    ''')
    # Open a new tk window and name it
    window = tk.Tk()
    window.title("Crow")
    window.geometry("800x500")
    # start the app
    CrowBase(window)
    window.mainloop()
