import Crow as C
class PrePull(C.tk.Frame):
    def __init__(self,name):
        #set up as tab
        C.tk.Frame.__init__(self,width=797,height=450)

        #lists to place collected data and files to get it from
        self.datafiles = []
        self.datalist = []

        #define pre-pull callback function
        def prepullcallback():
            #check if data files have been chosen
            if len(self.datafiles)==0:
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","No data files selected!")
            else:
                for file in self.datafiles:
                    print(file)

        #define select data callback function
        def selectdatacallback():
            self.datafiles = C.RequestFiles.RequestFiles("xml files","*.xml")

        #Pre-Pull button
        C.tk.Button(self,text="Pre-Pull",command=prepullcallback).place(x=80,y=80)
        
        #Select Data files button
        C.tk.Button(self,text="Select Data",command=selectdatacallback).place(x=150,y=80)