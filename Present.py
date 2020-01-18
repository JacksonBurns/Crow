#!/usr/bin/python3
import Crow as C
class Present(C.tk.Frame):
    def __init__(self,name):
        C.tk.Frame.__init__(self,width=47,height=450)
        def presentdatacallback():
            if '.xml' in str(C.globals.datafiles):
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Please select excel data files!")