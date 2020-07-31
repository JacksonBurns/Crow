from Crow_GC import Crow_GC as C


class Pull(C.tk.Frame):
    """
    Tab of the GC window responsible for pulling data from the entered
    xml files based on the indicated retention times and variability
    """

    def __init__(self, name):
        C.tk.Frame.__init__(self, width=47, height=450)
        # make place for collected retention times and tolerances to go
        # before being written
        self.rettimes = []
        self.toltimes = []

        # define clear entries callback
        def clearentriescallback():
            """
            Upon clicking clear entries button, removes all entered values for
            retention time and tolerance.
            """
            self.entryreadorclear("clear")

        def pulldatacallback():
            # gather the values in the entry boxes
            self.entryreadorclear("read")
            # check for wrong type of data file
            if ".xlsx" in str(C.globals_GC.datafiles):
                C.messagebox.showerror("Error!", "Please select raw data files.")
                return
            # check for missing tols or rt
            elif (len(self.rettimes) != len(self.toltimes)) or (
                len(self.rettimes) == 0 or len(self.toltimes) == 0
            ):
                C.tk.messagebox.showerror(
                    "Error!E", "At least one retention time/tolerance is missing."
                )
                return
            # break if non-chronological
            elif sorted(self.rettimes) != self.rettimes:
                C.tk.messagebox.showerror(
                    "Error!", "Retention times are not in chronological order.",
                )
                return
            # break if there is overlap in entered values also
            elif self.isthereoverlap():
                return
            elif len(C.globals_GC.datafiles) == 0:
                C.messagebox.showerror("Error!", "No raw data files selected.")
                return
            # after passing all validation, continue to remainder of method.
            # iterate through each and pull relevant data
            self.datalist = C.np.empty(  # empty array the size of len(datafile) x number of products
                [len(C.globals_GC.datafiles)-1, len(self.rettimes)], dtype=object
            )
            # iterate through each data test
            for file in C.globals_GC.datafiles:
                try:
                    # open file
                    temp = C.ParseXML.ParseXML(file)
                    # go to where peaks are stored
                    peaks = temp[C.globals_GC.peaktarg[0]][C.globals_GC.peaktarg[1]]
                    # setup a pair of lists to store information for
                    # peaks which fall within the window
                    peaksinwindow = []
                    # iterate through all the peaks
                    for peak in peaks[1:]:
                        # check if the peaks are the one we want
                        for i in range(0, len(self.rettimes)):
                            if (  # retention time - tolerance < limit
                                (
                                    float(peak[C.globals_GC.rettarg].text)
                                    - self.toltimes[i]
                                )
                                < self.rettimes[i]
                            ) & (  # retention time + tolerance > limit
                                (
                                    float(peak[C.globals_GC.rettarg].text)
                                    + self.toltimes[i]
                                )
                                > self.rettimes[i]
                            ):
                                # every time a valid peak is found, append its
                                # retention time and area to this list
                                peaksinwindow.append(
                                    tuple(
                                        [
                                            float(peak[C.globals_GC.rettarg].text),
                                            float(peak[C.globals_GC.areatarg].text),
                                            i,
                                        ]
                                    )
                                )
                    # assign area(s) to corresponding location in output array
                    # depending on selected peak picking method
                    for i in range(
                        0, len(self.rettimes)
                    ):  # go through in order of retention times
                        # pull out identified peaks for each retention time
                        poss = []
                        for suspect in peaksinwindow:
                            if suspect[2] == i:
                                poss.append(suspect[0:2])
                        if len(poss) == 0:
                            keep = "Not found"
                        elif len(poss) == 1:  # only one possible peak was found
                            if self.retinclude.get():
                                keep = poss[0]
                            else:
                                keep = poss[0][1]
                        elif (
                            self.pickingmethod.get() == 1
                        ):  # pick peak closest to the center of the window
                            possrettimes = [j[0] for j in poss]
                            possareas = [j[1] for j in poss]
                            if self.retinclude.get():
                                keep = poss[possrettimes.index(min(possrettimes, key=lambda x: abs(x-self.rettimes[i])))]
                            else:
                                keep = possareas[possrettimes.index(min(possrettimes, key=lambda x: abs(x-self.rettimes[i])))]
                        elif (
                            self.pickingmethod.get() == 2
                        ):  # keep max, just pick max area
                            if self.retinclude.get():
                                keep = max(poss, key=lambda x: x[1])
                            else:
                                keep = max([j[1] for j in poss])
                        elif self.pickingmethod.get() == 3:  # keep all areas
                            if self.retinclude.get():
                                keep = poss
                            else:
                                keep = [j[1] for j in poss]
                        else:
                            keep = "Error"
                        self.datalist[int(temp[C.globals_GC.welltarg[0]][C.globals_GC.welltarg[1]].text)-1, i] = str(keep).replace("\"", "").replace("]", "").replace("[", "")
                except IndexError as ie:
                    if C.globals_GC.debug:
                        C.globals_GC.mylog(ie)
                    warningmessage = (
                        "Please select files in order starting from 1 to end"
                    )
                    C.messagebox.showwarning(title="Warning", message=warningmessage)
                except Exception as e:
                    if C.globals_GC.debug:
                        C.globals_GC.mylog(e)
                    warningmessage = (
                        "No peak data found in file "
                        + str(file)
                        + "\n (possible failed injection)"
                    )
                    C.messagebox.showwarning(title="Warning", message=warningmessage)
            with open(C.globals_GC.exportdatapath + self.expname.get() + ".csv", "w") as file:
                # write header
                for i in range(len(self.rettimes)):
                    file.write("eluate "+str(i+1)+"\t")
                file.write("\n")
                # write all lines to a file in a tab separated value format
                for row in self.datalist:
                    for entry in row:
                        file.write(entry+"\t")
                    file.write("\n")
            msg = "Data successfully written to " + C.globals_GC.exportdatapath + self.expname.get() + ".csv"
            C.messagebox.showinfo(title="Data Written", message=msg)

        # pull data button
        C.tk.Button(self, text="Pull Requested Data", command=pulldatacallback).place(
            x=145, y=415
        )
        # set up button for picking method
        self.pickingmethod = C.tk.IntVar()
        methods = [("Keep Centermost", 1), ("Keep Maximum", 2), ("Keep All", 3)]
        C.tk.Label(self, text="Peak picking method:").place(x=150, y=305)
        yiterator = 325
        for i in range(len(methods)):
            C.tk.Radiobutton(
                self,
                text=methods[i][0],
                padx=10,
                variable=self.pickingmethod,
                value=methods[i][1],
            ).place(x=150, y=yiterator)
            yiterator += 30
        # set max as default selection
        self.pickingmethod.set(2)
        # set up chechbox for whether or not to include retention times
        self.retinclude = C.tk.IntVar()
        C.tk.Checkbutton(
            self,
            text='Include retention times?',
            variable=self.retinclude,
            onvalue=1,
            offvalue=0).place(
                x=280,
                y=415)

        # clear entries button
        C.tk.Button(self, text="Clear Entries", command=clearentriescallback).place(
            x=167, y=245
        )
        # Experiment Name Label
        C.tk.Label(self, text="Expt. Name:").place(x=85, y=280)
        # Experiment Name Entry Field
        self.expname = C.tk.Entry(self)
        self.expname.place(x=170, y=280)

        def add_entry_fields():
            C.tk.Label(self, text="Retention Time (minutes)").place(x=40, y=40)
            # assigning and placing have to be on seperate lines because place returns nothing
            self.rt1 = C.tk.Entry(self)
            self.rt1.place(x=40, y=65)
            self.rt2 = C.tk.Entry(self)
            self.rt2.place(x=40, y=90)
            self.rt3 = C.tk.Entry(self)
            self.rt3.place(x=40, y=115)
            self.rt4 = C.tk.Entry(self)
            self.rt4.place(x=40, y=140)
            self.rt5 = C.tk.Entry(self)
            self.rt5.place(x=40, y=165)
            self.rt6 = C.tk.Entry(self)
            self.rt6.place(x=40, y=190)
            self.rt7 = C.tk.Entry(self)
            self.rt7.place(x=40, y=215)
            # define tolerance entry fields
            C.tk.Label(self, text="Tolerance Time (minutes)").place(x=230, y=40)
            self.tol1 = C.tk.Entry(self)
            self.tol1.place(x=230, y=65)
            self.tol2 = C.tk.Entry(self)
            self.tol2.place(x=230, y=90)
            self.tol3 = C.tk.Entry(self)
            self.tol3.place(x=230, y=115)
            self.tol4 = C.tk.Entry(self)
            self.tol4.place(x=230, y=140)
            self.tol5 = C.tk.Entry(self)
            self.tol5.place(x=230, y=165)
            self.tol6 = C.tk.Entry(self)
            self.tol6.place(x=230, y=190)
            self.tol7 = C.tk.Entry(self)
            self.tol7.place(x=230, y=215)

        # define retention time fields and label
        add_entry_fields()

    def entryreadorclear(self, readorclear):
        if readorclear == "clear":
            self.rt1.delete(0, C.tk.END)
            self.tol1.delete(0, C.tk.END)
            self.rt2.delete(0, C.tk.END)
            self.tol2.delete(0, C.tk.END)
            self.rt3.delete(0, C.tk.END)
            self.tol3.delete(0, C.tk.END)
            self.rt4.delete(0, C.tk.END)
            self.tol4.delete(0, C.tk.END)
            self.rt5.delete(0, C.tk.END)
            self.tol5.delete(0, C.tk.END)
            self.rt6.delete(0, C.tk.END)
            self.tol6.delete(0, C.tk.END)
            self.rt7.delete(0, C.tk.END)
            self.tol7.delete(0, C.tk.END)
        else:
            try:
                self.rettimes = []
                self.toltimes = []
                if len(self.rt1.get()) > 0:
                    self.rettimes = self.rettimes + [float(self.rt1.get())]
                if len(self.tol1.get()) > 0:
                    self.toltimes = self.toltimes + [float(self.tol1.get())]
                if len(self.rt2.get()) > 0:
                    self.rettimes = self.rettimes + [float(self.rt2.get())]
                if len(self.tol2.get()) > 0:
                    self.toltimes = self.toltimes + [float(self.tol2.get())]
                if len(self.rt3.get()) > 0:
                    self.rettimes = self.rettimes + [float(self.rt3.get())]
                if len(self.tol3.get()) > 0:
                    self.toltimes = self.toltimes + [float(self.tol3.get())]
                if len(self.rt4.get()) > 0:
                    self.rettimes = self.rettimes + [float(self.rt4.get())]
                if len(self.tol4.get()) > 0:
                    self.toltimes = self.toltimes + [float(self.tol4.get())]
                if len(self.rt5.get()) > 0:
                    self.rettimes = self.rettimes + [float(self.rt5.get())]
                if len(self.tol5.get()) > 0:
                    self.toltimes = self.toltimes + [float(self.tol5.get())]
                if len(self.rt6.get()) > 0:
                    self.rettimes = self.rettimes + [float(self.rt6.get())]
                if len(self.tol6.get()) > 0:
                    self.toltimes = self.toltimes + [float(self.tol6.get())]
                if len(self.rt7.get()) > 0:
                    self.rettimes = self.rettimes + [float(self.rt7.get())]
                if len(self.tol7.get()) > 0:
                    self.toltimes = self.toltimes + [float(self.tol7.get())]
            except Exception as e:
                if C.globals_GC.debug:
                    C.globals_GC.mylog(e)
                C.messagebox.showerror(
                    "Error!", "Invalid retetion time/tolerance time entered.",
                )

    def isthereoverlap(self):
        if len(self.rettimes) == 1:
            return False
        else:
            # iterate through list and check for overlap
            for i in range(1, len(self.rettimes)):
                # print(self.rettimes[i])
                if (self.rettimes[i] - self.toltimes[i]) <= (
                    self.rettimes[i - 1] + self.toltimes[i - 1]
                ):
                    # send error with which retention times overlap
                    C.tk.messagebox.showerror(
                        "Error!",
                        "Retention time/tolerance "
                        + str(i)
                        + " overlaps "
                        + str(i + 1)
                        + ".",
                    )
                    return True
