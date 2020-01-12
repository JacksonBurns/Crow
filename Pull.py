import tkinter as tk
class Pull(tk.Frame):
    def __init__(self,name):
       tk.Frame.__init__(self,width=797,height=450)
       self.label = tk.Label(self, text="Mike Hunt")
       self.label.place(x=69,y=69)