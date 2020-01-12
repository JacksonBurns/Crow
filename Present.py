import Crow as C
class Present(C.tk.Frame):
    def __init__(self,name):
       C.tk.Frame.__init__(self,width=797,height=450)
       self.label = C.tk.Label(self, text="Ben Dover")
       self.label.place(x=69,y=69)