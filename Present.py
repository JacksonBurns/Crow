import Crow_GC as C
class Present(C.tk.Frame):
    def __init__(self,name):
        C.tk.Frame.__init__(self,width=47,height=450)
        #function for present button push, handles error checking and reading state of buttons
        def presentdatacallback():
            #check for wrong type of data selected
            if '.xml' in str(C.globals.datafiles):
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Please select excel data file (.csv)!")
            #please select data
            elif len(C.globals.datafiles) == 0:
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Please select excel data file (.csv)!")
            #please select only one excel file at a time
            elif len(C.globals.datafiles) != 1:
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Please select an excel data file (.csv)!")
            #if passes all tests, present accordingly
            else:
                #pull data from user
                exceldata = C.np.genfromtxt(C.globals.datafiles[0], dtype=float, delimiter=',', names=True)
                #decide on colormap from color radio buttons
                
                
                #call graphic generator appropriately
                
        def graphic_generator():
            pass
                
                
                
                
        #make present data button
        C.tk.Button(self,text="Present",command=presentdatacallback).place(relx=0.4,rely=0.9)
        #make radio buttons for well layout
        layout = C.tk.IntVar()
        layouts = [("96 (8x12)",1),("96 (12x8)",2),("24 (4x6)",3),("24 (6x4)",4)]
        C.tk.Label(self,text="Well layout:").place(x=5,y=40)
        yiterator=60
        for i in range(len(layouts)):
            C.tk.Radiobutton(self,text=layouts[i][0],indicatoron=0,padx = 10,variable=layout,value=layouts[i][1]).place(x=5,y=yiterator)
            yiterator+=25
        
        #make radio buttons for graphic color
        colorscheme = C.tk.IntVar()
        colorschemes = [("neutral",1),("bright",2),("dark",3),("deuteranomaly",4),("custom",5)]
        C.tk.Label(self,text="Color scheme:").place(x=130,y=40)
        yiterator=60
        for i in range(len(colorschemes)):
            C.tk.Radiobutton(self,text=colorschemes[i][0],indicatoron=0,padx = 10,variable=colorscheme,value=colorschemes[i][1]).place(x=130,y=yiterator)
            yiterator+=25   
        
        #make radio buttons for datafilters
        datafilter = C.tk.IntVar()
        datafilters = [("none",1),("exclude threshold",2),("shade by yield",3),("set cutoffs",4)]
        C.tk.Label(self,text="Data filter:").place(x=255,y=40)
        yiterator=60
        for i in range(len(datafilters)):
            C.tk.Radiobutton(self,text=datafilters[i][0],indicatoron=0,padx = 10,variable=datafilter,value=datafilters[i][1]).place(x=255,y=yiterator)
            yiterator+=25  
        
        