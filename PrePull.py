import Crow as C
import matplotlib.pyplot as plot
class PrePull(C.tk.Frame):
    def __init__(self,name):
        #set up as tab
        C.tk.Frame.__init__(self,width=797,height=450)

        #lists to place collected data and files to get it from
        self.datafiles = []
        self.datadict = {}
        self.FileDisplay = C.tk.StringVar()
        self.FileDisplay = ""
        #define pre-pull callback function
        def prepullcallback():
            #check if data files have been chosen
            if len(self.datafiles)==0:
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","No data files selected!")
            else:
                #iterate through each and pull relevant data
                self.datadict = {}
                for file in self.datafiles:
                    temp = C.ParseXML.ParseXML(file)
                    temp = temp[4][2]
                    for peak in temp[1:]:
                        rettime = round(float(peak[4].text),2)
                        if (rettime in self.datadict):
                            self.datadict[rettime]+=1
                        else:
                            self.datadict[rettime]=1
                #display the histogram
                plot.bar(list(self.datadict.keys()),list(self.datadict.values()), width=0.005)
                plot.ylabel("Number of Wells")
                plot.xlabel("Retention Time (minutes)")
                plot.show()
                #self.datadict.keys()

        #define select data callback function
        def selectdatacallback():
            self.datafiles = C.RequestFiles.RequestFiles("xml files","*.xml")
            self.FileDisplay = str(self.datafiles).replace(",","\n").replace("(","").replace(")","")
            update_files()

        #Pre-Pull button
        C.tk.Button(self,text="Generate histogram",command=prepullcallback).place(x=80,y=40)
        #data files label
        C.tk.Label(self,text="Current Data Files:").place(x=250,y=40)
        #data files display
        def update_files():
            temp = C.tk.Text(master=self,height=10,width=40)
            temp.insert(C.tk.END,str(len(self.datafiles))+" TOTAL FILES\n"+self.FileDisplay)
            temp.place(x=250,y=65)
            temp.config(state="disabled")
        update_files()
        #Select Data files button
        C.tk.Button(self,text="Select Data",command=selectdatacallback).place(x=105,y=80)