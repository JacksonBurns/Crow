from os import chdir
import Crow
chdir(r"C:\Users\jwb1j\OneDrive\Documents\GitHub\Crow")
root = Crow.ParseXML.ParseXML('SampleData.xml')
for child in root:  
    print(child)