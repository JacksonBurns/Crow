import Crow_GC as C
import matplotlib.pyplot as plot
class PrePull(C.tk.Frame):
    def __init__(self,name):
        #set up as tab
        C.tk.Frame.__init__(self,width=460,height=450)
        #lists to place collected data and files to get it from
        self.datadict = {}
        #define pre-pull callback function
        def prepullcallback():
            #check if data files have been chosen
            if len(C.globals.datafiles)==0:
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","No data files selected!")
            elif '.xlsx' in str(C.globals.datafiles):
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Please select raw data files!")
            else:
                #iterate through each and pull relevant data
                self.datadict = {}
                for file in C.globals.datafiles:
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
        #Pre-Pull button
        C.tk.Button(self,text="Generate Histogram",command=prepullcallback).place(relx=0.3,rely=0.35)