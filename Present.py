#!/usr/bin/python3
import Crow as C
class Present(C.tk.Frame):
    def __init__(self,name):
        C.tk.Frame.__init__(self,width=47,height=450)
        def presentdatacallback():
            if '.xml' in str(C.globals.datafiles):
                C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Please select excel data files!")
                
                
                
                
        #make present data button
        C.tk.Button(self,text="Present",command=presentdatacallback).place(relx=0.4,rely=0.9)
        #make radio buttons for well layout
        layout = C.tk.IntVar()
        layouts = [("96 (8x12)",1),("96 (12x8)",2),("24 (4x8)",3),("24 (8x4)",4)]
        C.tk.Label(self,text="Well layout:").place(x=5,y=40)
        yiterator=60
        for i in range(len(layouts)):
            C.tk.Radiobutton(self,text=layouts[i][0],indicatoron=0,padx = 10,variable=layout,value=layouts[i][1]).place(x=5,y=yiterator)
            yiterator+=25
        
        #make radio buttons for graphic color
        colorscheme = C.tk.IntVar()
        colorschemes = [("neutral",1),("bright",2),("dark",3),("deuteranomaly",4)]
        C.tk.Label(self,text="Color scheme:").place(x=130,y=40)
        yiterator=60
        for i in range(len(layouts)):
            C.tk.Radiobutton(self,text=colorschemes[i][0],indicatoron=0,padx = 10,variable=colorscheme,value=colorschemes[i][1]).place(x=130,y=yiterator)
            yiterator+=25   
        
        #make radio buttons for datafilters
        datafilter = C.tk.IntVar()
        datafilters = [("none",1),("exclude threshold",2),("shade by yield",3),("set groups",4)]
        C.tk.Label(self,text="Data filter:").place(x=255,y=40)
        yiterator=60
        for i in range(len(layouts)):
            C.tk.Radiobutton(self,text=datafilters[i][0],indicatoron=0,padx = 10,variable=datafilter,value=datafilters[i][1]).place(x=255,y=yiterator)
            yiterator+=25  
        
        
            