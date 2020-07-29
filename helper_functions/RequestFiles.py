from tkinter import filedialog, Tk


def RequestFiles(file_desc, file_ext, path):
    """
    Open a new tkinter root window and use the pre-existing file dialog
    to retrieve a file of type file_ext (described by file_desc),
    path specifies starting directory

    file_desc: string containing a description of the file to be chosen, ex. "Text Document"
    file_ext: string of OS file extension, filetype ex. ".txt"
    path: string giving location to start at with the file doalog, ex. "/usr/jackson/Desktop"
    """
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilenames(
        initialdir=path, title="Select files", filetypes=[(file_desc, file_ext)]
    )
    return root.filename
