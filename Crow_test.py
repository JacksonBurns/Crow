import Crow as C
#C.Crow()
from os import chdir
chdir(r"C:\Users\jwb1j\OneDrive\Documents\GitHub\Crow")
root = C.ParseXML.ParseXML('SampleData.xml')
for child in root:  
    print(child)

import tkinter
root = tkinter.Tk()
my_gui = C.Crow(root)
root.mainloop()