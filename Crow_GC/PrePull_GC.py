from Crow_GC import Crow_GC as C


class PrePull(C.tk.Frame):
    """
    Tab which contains functionality of pre-pulling, which involves
    parsing all entered data files and creating a histogram
    """

    def __init__(self, name):
        # set up as tab
        C.tk.Frame.__init__(self, width=460, height=450)
        # lists to place collected data and files to get it from
        self.datadict = {}

        # define pre-pull callback function
        def prepullcallback():
            """
            When the "Generate Histogram" button is pushed, parse through
            every data file, bin the results, and plot.
            """
            # check if data files have been chosen
            if len(C.globals_GC.datafiles) == 0:
                C.messagebox.showerror("Error!", "No .xml data files selected.")
            elif ".xlsx" in str(C.globals_GC.datafiles):
                C.messagebox.showerror(
                    "Error!", "Please select raw data files, not processed excel data!"
                )
            else:
                # iterate through each and pull relevant data
                self.datadict = {}
                for file in C.globals_GC.datafiles:
                    try:
                        temp = C.ParseXML.ParseXML(file)
                        temp = temp[C.globals_GC.peaktarg[0]][C.globals_GC.peaktarg[1]]
                        for peak in temp[1:]:
                            rettime = round(float(peak[C.globals_GC.rettarg].text), 2)
                            if rettime in self.datadict:
                                self.datadict[rettime] += 1
                            else:
                                self.datadict[rettime] = 1
                    except Exception as e:
                        warningmessage = (
                            "No peak data found in file "
                            + str(file)
                            + "\n (possible failed injection)"
                        )
                        C.messagebox.showwarning(
                            title="Warning", message=warningmessage
                        )
                # display the histogram
                C.plot.bar(
                    list(self.datadict.keys()),
                    list(self.datadict.values()),
                    width=C.globals_GC.roundres,
                )
                C.plot.ylabel("Number of Wells")
                C.plot.xlabel("Retention Time (minutes)")
                C.plot.show()

        # Pre-Pull button
        C.tk.Button(self, text="Generate Histogram", command=prepullcallback).place(
            relx=0.3, rely=0.35
        )
