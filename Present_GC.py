import Crow_GC as C
import matplotlib.pyplot as plot
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
                #check for files that are too big
                if len(exceldata[0])>10:
                    C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Data has too many columns (>10)!")
                #decide on colorscheme from color radio buttons
                if colorscheme.get()==1: #neutral
                    totalcolormap=C.np.array([[1,1,1],[1,0.1,0.1],[1,0.753,0],[0.573,0.816,0.314],[0.5,0.5,0.5],[0,0,0.8],[1,0.55,0],[1,0.5,1],[0.4,0.8,1],[0.2,0.1,0.1]])
                elif colorscheme.get()==2: #bright
                    totalcolormap=C.np.array([[1,1,1],[0,1,1],[1,1,0],[0,1,0],[0,0,1],[1,0,0],[1,0.6,0],[1,0,1],[0.5,0.5,0.5],[0,0.5,0.6]])
                elif colorscheme.get()==3: #colorblind-friendly
                    totalcolormap=C.np.array([[0.165,0.219,0.404],[0.545,0.498,0.278],[0.612,0.620,0.710],[0.980,0.949,0.918],[1,0.427,0.741]])
                elif colorscheme.get()==4: #custom colors
                    print("JACKSON PROGRAM THIS ONE TOO")
                    pass
                #call graphic generator appropriately
                # 96 (8x12)
                if layout.get()==1: 
                    #try:
                    graphic_generator(exceldata,[8,12],['A','B','C','D','E','F','G','H'],[0.1,0.95],0.05,['1','2','3','4','5','6','7','8','9','10','11','12'],[0.1,0.8],0.05,totalcolormap)
                    #except:
                    #    C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Something went wrong, please try again!")
                # 96 (12x8)
                elif layout.get()==2: 
                    #try:
                    print("JACKSON PROGRAM THIS ONE")
                        #graphic_generator()
                    #except:
                    #    C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Something went wrong, please try again!")
                # 24 (4x6)
                elif layout.get()==3: 
                    #try:
                    graphic_generator(exceldata,[4,6],['A','B','C','D'],[0.17,0.118],0.22,['1','2','3','4','5','6'],[0.175,0.935],0.1342,totalcolormap)
                    #except:
                    #    C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Something went wrong, please try again!")
                # 24 (6x4)
                elif layout.get()==4: 
                    #try:
                    graphic_generator(exceldata,[6,4],['A','B','C','D','E','F'],[0.17,0.118],0.142,['1','2','3','4'],[0.168,0.97],0.2055,totalcolormap)
                    #except:
                    #    C.messagebox.showerror("Error SCIENCE FICTION REFERENCE","Something went wrong, please try again!")
        def graphic_generator(exceldata,subplotdims,letters,heightstarters,heightiterator,numbers,widthstarters,widthiterator,totalcolormap):
            myfig, subplt = plot.subplots(subplotdims[0],subplotdims[1])
            
            ax = myfig.gca()
            count = 0
            for letter in letters:
                ax.annotate(letter,xy=(heightstarters[0],heightstarters[1]-count*heightiterator),xycoords='figure fraction')
                count+=1
            count = 0
            for number in numbers:
                ax.annotate(number,xy=(widthstarters[0]+count*widthiterator,widthstarters[1]),xycoords='figure fraction')
                count+=1
                
            for wellnum in range(0,subplotdims[0]*subplotdims[1]):
                row = wellnum//subplotdims[1]
                col = wellnum%subplotdims[1]
                subplt[row,col].pie(C.np.array(list(exceldata[wellnum])/min(list(exceldata[wellnum]))) , 
                      colors=totalcolormap , 
                      wedgeprops = {'linewidth':1,'edgecolor':[0,0,0]} , 
                      radius=1.3 , 
                      counterclock=False)
                subplt[row,col].axis('off')
                #subplt[row,col].set_title(str(wellnum+1))
                
            
            
            myfig.show()
        
                
                
                
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
        colorschemes = [("neutral",1),("bright",2),("deuteranomaly",3),("custom",4)]
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
        