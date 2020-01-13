import Crow as C
class Pull(C.tk.Frame):
    def __init__(self,name):
        C.tk.Frame.__init__(self,width=797,height=450)
        #lists to place collected data and files to get it from
        self.datafiles = []
        self.datadict = {}
        self.FileDisplay = C.tk.StringVar()
        self.FileDisplay = ""
        #make place for collected retention times and tolerances to go
        self.rettimes = []
        self.toltimes = []
        #define clear entries callback
        def clearentriescallback():
            self.entryreadorclear("clear")
        #define select data callback function
        def selectdatacallback():
            self.datafiles = C.RequestFiles.RequestFiles("xml files","*.xml")
            self.FileDisplay = str(self.datafiles).replace(",","\n").replace("(","").replace(")","")
            update_files()
        
        #define pull data callback function
        def pulldatacallback():
            #gather the values in the entry boxes
            #print("rt: "+self.rt1.get() + " tol: " + self.tol1.get())
            self.entryreadorclear("read")
            #check for missing tols or rt, error at least one rt/tol pair is missing a member
            print(self.rettimes)
            print(self.toltimes)
        #data files label
        C.tk.Label(self,text="Current Data Files:").place(x=50,y=40)
        #data files display
        def update_files():
            temp = C.tk.Text(master=self,height=10,width=40)
            temp.insert(C.tk.END,str(len(self.datafiles))+" TOTAL FILES\n"+self.FileDisplay)
            temp.place(x=50,y=65)
            temp.config(state="disabled")
        update_files()
        #Select Data files button
        C.tk.Button(self,text="Select Data",command=selectdatacallback).place(x=50,y=245)
        #pull data button
        C.tk.Button(self,text="Pull Requested Data",command=pulldatacallback).place(x=500,y=245)
        C.tk.Button(self,text="Clear Entries",command=clearentriescallback).place(x=525,y=280)
        def add_entry_fields():
            C.tk.Label(self,text="Retention Time (minutes)").place(x=420,y=40)
            #assigning and placing have to be on seperate lines because place returns nothing
            self.rt1 = C.tk.Entry(self)
            self.rt1.place(x=420,y=65)
            self.rt2 = C.tk.Entry(self)
            self.rt2.place(x=420,y=90)
            self.rt3 = C.tk.Entry(self)
            self.rt3.place(x=420,y=115)
            self.rt4 = C.tk.Entry(self)
            self.rt4.place(x=420,y=140)
            self.rt5 = C.tk.Entry(self)
            self.rt5.place(x=420,y=165)
            self.rt6 = C.tk.Entry(self)
            self.rt6.place(x=420,y=190)
            self.rt7 = C.tk.Entry(self)
            self.rt7.place(x=420,y=215)
            #define tolerance entry fields
            C.tk.Label(self,text="Tolerance Time (minutes)").place(x=570,y=40)
            self.tol1 = C.tk.Entry(self)
            self.tol1.place(x=570,y=65)
            self.tol2 = C.tk.Entry(self)
            self.tol2.place(x=570,y=90)
            self.tol3 = C.tk.Entry(self)
            self.tol3.place(x=570,y=115)
            self.tol4 = C.tk.Entry(self)
            self.tol4.place(x=570,y=140)
            self.tol5 = C.tk.Entry(self)
            self.tol5.place(x=570,y=165)
            self.tol6 = C.tk.Entry(self)
            self.tol6.place(x=570,y=190)
            self.tol7 = C.tk.Entry(self)
            self.tol7.place(x=570,y=215)
        #define retention time fields and label
        add_entry_fields()
    def entryreadorclear(self,readorclear):
        if readorclear=="clear":
            self.rt1.delete(0,C.tk.END)
            self.tol1.delete(0,C.tk.END)
            self.rt2.delete(0,C.tk.END)
            self.tol2.delete(0,C.tk.END)
            self.rt3.delete(0,C.tk.END)
            self.tol3.delete(0,C.tk.END)
            self.rt4.delete(0,C.tk.END)
            self.tol4.delete(0,C.tk.END)
            self.rt5.delete(0,C.tk.END)
            self.tol5.delete(0,C.tk.END)
            self.rt6.delete(0,C.tk.END)
            self.tol6.delete(0,C.tk.END)
            self.rt7.delete(0,C.tk.END)
            self.tol7.delete(0,C.tk.END)
        else:
            try:
                self.rettimes = []
                self.toltimes = []
                if (len(self.rt1.get())>0):
                    self.rettimes = self.rettimes + [float(self.rt1.get())]
                if (len(self.tol1.get())>0):
                    self.toltimes = self.toltimes + [float(self.tol1.get())]
                if (len(self.rt2.get())>0):
                    self.rettimes = self.rettimes + [float(self.rt2.get())]
                if (len(self.tol2.get())>0):
                    self.toltimes = self.toltimes + [float(self.tol2.get())]
                if (len(self.rt3.get())>0):
                    self.rettimes = self.rettimes + [float(self.rt3.get())]
                if (len(self.tol3.get())>0):
                    self.toltimes = self.toltimes + [float(self.tol3.get())]
                if (len(self.rt4.get())>0):
                    self.rettimes = self.rettimes + [float(self.rt4.get())]
                if (len(self.tol4.get())>0):
                    self.toltimes = self.toltimes + [float(self.tol4.get())]
                if (len(self.rt5.get())>0):
                    self.rettimes = self.rettimes + [float(self.rt5.get())]
                if (len(self.tol5.get())>0):
                    self.toltimes = self.toltimes + [float(self.tol5.get())]
                if (len(self.rt6.get())>0):
                    self.rettimes = self.rettimes + [float(self.rt6.get())]
                if (len(self.tol6.get())>0):
                    self.toltimes = self.toltimes + [float(self.tol6.get())]
                if (len(self.rt7.get())>0):
                    self.rettimes = self.rettimes + [float(self.rt7.get())]
                if (len(self.tol7.get())>0):
                    self.toltimes = self.toltimes + [float(self.tol7.get())]
            except:
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Invalid retetion time/tolerance time entered!")



