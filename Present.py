import tkinter as tk
class Present(tk.Frame):
    def __init__(self,name):
       tk.Frame.__init__(self,width=797,height=450)
       self.label = tk.Label(self, text="Ben Dover")
       self.label.place(x=69,y=69)