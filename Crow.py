#This is the wrapper function for Crow

#retrieve python packages that aren't built in for some stupid reason
import os
import tkinter

#retrieve my functions written elsewhere
import ParseXML as ParseXML
'''
#maww
def Crow():
    print("maww")
    return 0
'''
#define GUI
class Crow:
    def __init__(self, master):
        #idk what this does really
        self.master = master
        master.title("Crow - GC")
        #title on top of window
        self.label = tkinter.Label(master, text="Crow Really Outta Work")
        self.label.pack()
        #create button for crow sound
        self.call_button = tkinter.Button(master, text="Call", command=self.call)
        self.call_button.pack()
        #create button for saying goodbye to the crow
        self.close_button = tkinter.Button(master, text="Close", command=master.quit)
        self.close_button.pack()
    #crow call function
    def call(self):
        print("maww")
