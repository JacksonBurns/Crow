#!/usr/bin/python3
import Crow as C
class Present(C.tk.Frame):
    def __init__(self,name):
        C.tk.Frame.__init__(self,width=797,height=450)
        #place to store input data and the file names
        self.datafiles = []
        self.FileDisplay = C.tk.StringVar()
        self.FileDisplay = ""
        #define select data callback function
        def selectdatacallback():
            self.datafiles = C.RequestFiles.RequestFiles("xml files","*.xml")
            self.FileDisplay = str(self.datafiles).replace(",","\n").replace("(","").replace(")","")
            update_files()
        #data files display
        def update_files():
            temp = C.tk.Text(master=self,height=10,width=40)
            temp.insert(C.tk.END,str(len(self.datafiles))+" TOTAL FILES\n"+self.FileDisplay)
            temp.place(x=50,y=65)
            temp.config(state="disabled")
        update_files()
        #data files label
        C.tk.Label(self,text="Current Data Files:").place(x=50,y=40)
        #Select Data files button
        C.tk.Button(self,text="Select Data",command=selectdatacallback).place(x=50,y=245)