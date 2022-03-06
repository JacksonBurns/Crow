import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plot

from crow.utils import ParseXML
from crow.utils.logger import mylog


class PrePull(tk.Frame):
    """
    Tab which contains functionality of pre-pulling, which involves
    parsing all entered data files and creating a histogram
    """

    def __init__(self, name, crow_globals):
        # set up as tab
        tk.Frame.__init__(self, width=460, height=450)
        # lists to place collected data and files to get it from
        self.datadict = {}

        # define pre-pull callback function
        def prepullcallback():
            """
            When the "Generate Histogram" button is pushed, parse through
            every data file, bin the results, and plot.
            """
            # check if data files have been chosen
            if len(crow_globals.datafiles) == 0:
                messagebox.showerror("Error!", "No .xml data files selected.")
            elif ".csv" in str(crow_globals.datafiles):
                messagebox.showerror(
                    "Error!", "Please select raw data files, not processed excel data!"
                )
            else:
                # iterate through each and pull relevant data
                self.datadict = {}
                for file in crow_globals.datafiles:
                    try:
                        temp = ParseXML.ParseXML(file)
                        temp = temp[crow_globals.peaktarg[0]
                                    ][crow_globals.peaktarg[1]]
                        for peak in temp[1:]:
                            rettime = round(
                                float(peak[crow_globals.rettarg].text), 2)
                            if rettime in self.datadict:
                                self.datadict[rettime] += 1
                            else:
                                self.datadict[rettime] = 1
                    except Exception as e:
                        if crow_globals.debug:
                            mylog(e)
                        warningmessage = (
                            "No peak data found in file "
                            + str(file)
                            + "\n (possible failed injection)"
                        )
                        messagebox.showwarning(
                            title="Warning", message=warningmessage)
                # display the histogram
                plot.bar(
                    list(self.datadict.keys()),
                    list(self.datadict.values()),
                    width=crow_globals.roundres,
                )
                plot.ylabel("Number of Wells")
                plot.xlabel("Retention Time (minutes)")
                plot.show()

        # Pre-Pull button
        self.prepullbutton = tk.Button(
            self, text="Generate Histogram", command=prepullcallback,
        )
        self.prepullbutton.place(
            relx=0.3, rely=0.35
        )
