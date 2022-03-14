from tkinter import filedialog, Tk


def RequestFiles(file_desc, file_ext, path):
    """
    Open a new tkinter root window and use the pre-existing file dialog
    to retrieve a file of type file_ext (described by file_desc),
    path specifies starting directory

    Args:
        file_desc (string): description of the file to be chosen, ex. "Text Document"
        file_ext (string): OS file extension, filetype ex. ".txt"
        path (string): location to start at with the file doalog, ex. "/usr/jackson/Desktop"

    Returns:
        list(string): List of files selected by the user.
    """
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilenames(
        initialdir=path, title="Select files", filetypes=[(file_desc, file_ext)]
    )
    return root.filename
