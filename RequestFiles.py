from tkinter import filedialog, Tk
def RequestFiles(file_desc,file_ext):
    root = Tk()
    root.filename =  filedialog.askopenfilenames(initialdir = r"C:\Users\jwb1j\OneDrive\Desktop\hte input data",title = "Select files",filetypes = [(file_desc,file_ext)])
    return (root.filename)