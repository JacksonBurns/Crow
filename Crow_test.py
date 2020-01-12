import Crow
import time
#C.Crow()
from os import chdir
chdir(r"C:\Users\jwb1j\OneDrive\Documents\GitHub\Crow")
root = Crow.ParseXML.ParseXML('SampleData.xml')
for child in root:  
    print(child)

import tkinter
root = tkinter.Tk()
my_gui = Crow.Crow(root)
root.mainloop()

time.sleep(3)
my_gui.update_warning("anime is danger!")
my_gui.call()