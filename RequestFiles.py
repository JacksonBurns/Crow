#!/usr/bin/python3.6
from tkinter import filedialog, Tk


def RequestFiles(file_desc, file_ext, path):
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilenames(
        initialdir=path, title="Select files", filetypes=[(file_desc, file_ext)]
    )
    return root.filename

