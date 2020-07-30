from Crow_GC import Crow_GC as C


class Present(C.tk.Frame):
    """
    Tab of the GC window resposible for taking columns
    of processed data and generating pie charts of the results,
    including various filters and color schemes.
    """

    def __init__(self, name):
        C.tk.Frame.__init__(self, width=47, height=450)

        # begin defintiion of callbacks, followed by user interface
        def presentdatacallback():
            """
            Upon clicking the present data button, validate input and
            then read state of UI buttons to determine settings
            """
            # check for wrong type of data selected
            if ".xml" in str(C.globals_GC.datafiles):
                C.messagebox.showerror(
                    "Error!", "Please select excel data file (.csv)!",
                )
                return
            # please select data
            elif len(C.globals_GC.datafiles) == 0:
                C.messagebox.showerror(
                    "Error!", "Please select excel data file (.csv)!",
                )
                return
            # please select only one excel file at a time
            elif len(C.globals_GC.datafiles) != 1:
                C.messagebox.showerror(
                    "Error!", "Please select a single excel data file (.csv)!",
                )
                return
            # if passes all tests, present accordingly
            # pull data from user entered file
            exceldata = C.np.genfromtxt(
                C.globals_GC.datafiles[0], dtype=float, delimiter=",", names=True
            )
            # check for files that are too big
            if len(exceldata[0]) > 9:
                C.messagebox.showerror(
                    "Error!", "Data has too many columns (>10).",
                )
            # decide on colorscheme from color radio buttons
            if colorscheme.get() == 1:  # neutral
                totalcolormap = C.np.array(
                    [
                        [1, 1, 1],
                        [1, 0.1, 0.1],
                        [1, 0.753, 0],
                        [0.573, 0.816, 0.314],
                        [0.5, 0.5, 0.5],
                        [0, 0, 0.8],
                        [1, 0.55, 0],
                        [1, 0.5, 1],
                        [0.4, 0.8, 1],
                        [0.2, 0.1, 0.1],
                    ]
                )
            elif colorscheme.get() == 2:  # bright
                totalcolormap = C.np.array(
                    [
                        [1, 1, 1],
                        [0, 1, 1],
                        [1, 1, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                        [1, 0, 0],
                        [1, 0.6, 0],
                        [1, 0, 1],
                        [0.5, 0.5, 0.5],
                        [0, 0.5, 0.6],
                    ]
                )
            elif colorscheme.get() == 3:  # colorblind-friendly
                totalcolormap = C.np.array(
                    [
                        [0.165, 0.219, 0.404],
                        [0.545, 0.498, 0.278],
                        [0.612, 0.620, 0.710],
                        [0.980, 0.949, 0.918],
                        [1, 0.427, 0.741],
                    ]
                )
            elif colorscheme.get() == 4:  # custom colors
                totalcolormap = []
                for i in range(0, len(exceldata[0])):
                    rgb, _ = C.cc.askcolor(
                        parent=self, title="Choose color " + str(i + 1)
                    )
                    totalcolormap = totalcolormap + [C.np.array(list(rgb)) / 256]
            else:
                C.messagebox.showerror(
                    "Error!", "Please select a color scheme!",
                )
                return
            # call graphic generator appropriately
            # 96 (8x12)
            if layout.get() == 1:
                try:
                    graphic_generator(exceldata, [8, 12], totalcolormap, (6, 4))
                except Exception as e:
                    if C.globals_GC.debug:
                        C.globals_GC.mylog(e)
                    C.messagebox.showerror(
                        "Error!", "Something went wrong, please try again.",
                    )
            # 96 (12x8)
            elif layout.get() == 2:
                try:
                    graphic_generator(exceldata, [12, 8], totalcolormap, (4, 6))
                except Exception as e:
                    if C.globals_GC.debug:
                        C.globals_GC.mylog(e)
                    C.messagebox.showerror(
                        "Error!", "Something went wrong, please try again.",
                    )
            # 24 (4x6)
            elif layout.get() == 3:
                try:
                    graphic_generator(exceldata, [4, 6], totalcolormap, (6, 4))
                except Exception as e:
                    if C.globals_GC.debug:
                        C.globals_GC.mylog(e)
                    C.messagebox.showerror(
                        "Error!", "Something went wrong, please try again.",
                    )
            # 24 (6x4)
            elif layout.get() == 4:
                try:
                    graphic_generator(exceldata, [6, 4], totalcolormap, (4, 6))
                except Exception as e:
                    if C.globals_GC.debug:
                        C.globals_GC.mylog(e)
                    C.messagebox.showerror(
                        "Error!", "Something went wrong, please try again.",
                    )
            else:
                C.messagebox.showerror("Error!", "Please select a layout.")

        def graphic_generator(exceldata, subplotdims, totalcolormap, dims):
            """
            general purpose, abstract function for the generation of hte
            diagrams
            first check for which data filter has been selected, then
            moves on to plotting.

            exceldata: numpy array-type of the values to be plotted
            subplotdims: array of ints containing length and width of the
                            experiment
            totalcolormap: array of floats containing colors to be used in the
                            diagram
            dims: tuple, immutable version of the dimensions of the subplot
                            in the order required by matplotlib
            """
            # Check for which filter the user has requested, and call the
            # appropriate pop-up window
            if datafilter.get() == 2:  # exclude threshold
                self.excludePopup = excludePopup(self.master)
                self.master.wait_window(self.excludePopup.top)
            elif datafilter.get() == 3:  # shade by yield
                # popup to ask which column the chemical the gradient should be based off of is in
                self.shadebyyieldPopup = shadebyyieldPopup(self.master)
                self.master.wait_window(self.shadebyyieldPopup.top)
                excludeColmax = max(
                    [
                        well[int(self.shadebyyieldPopup.shadecol) - 1]
                        for well in exceldata
                    ]
                )
            elif datafilter.get() == 4:  # set cutoffs
                # find out how many groups to make
                self.numberofcutoffsPopup = numberofcutoffsPopup(self.master)
                self.master.wait_window(self.numberofcutoffsPopup.top)
                cutoffvalues = []
                cutoffcolors = []
                for i in range(0, int(self.numberofcutoffsPopup.numgroups)):
                    self.cutoffPopup = cutoffPopup(self.master)
                    self.master.wait_window(self.cutoffPopup.top)
                    # assign values before overwritten
                    cutoffvalues = cutoffvalues + [float(self.cutoffPopup.cutoffval)]
                    cutoffcolors = cutoffcolors + [
                        [int(s) / 255 for s in self.cutoffPopup.cutoffcolor.split(",")]
                    ]
            # create figure with correct number of subplots
            myfig, subplt = C.plot.subplots(
                subplotdims[0], subplotdims[1], figsize=dims
            )
            for wellnum in range(0, subplotdims[0] * subplotdims[1]):
                # go to position
                row = wellnum // subplotdims[1]
                col = wellnum % subplotdims[1]
                # well data
                welldata = exceldata[wellnum]
                if datafilter.get() == 2:  # exclude threshold
                    try:
                        if welldata[int(self.excludePopup.excludecol) - 1] < float(
                            self.excludePopup.excludeval
                        ):  # exclude cutoff
                            subplt[row, col].pie([0])
                        else:
                            # handle wells where one or more pie slices are zero
                            temp = totalcolormap.copy()
                            # iterate through list
                            mask = []
                            for idx, pievalue in enumerate(welldata):
                                # each time a zero is found, take index and remove corresponding color from temp of colormap
                                if float(pievalue) == 0:
                                    mask = mask + [idx]
                            if len(mask) != 0:
                                temp = C.np.delete(temp, mask, 0)
                                welldata = [
                                    val
                                    for idx, val in enumerate(welldata)
                                    if idx not in mask
                                ]
                            subplt[row, col].pie(
                                C.np.array(list(welldata) / min(list(welldata))),
                                colors=temp,
                                wedgeprops={"linewidth": 1, "edgecolor": [0, 0, 0]},
                                radius=1.3,
                                counterclock=False,
                            )
                    except Exception as e:
                        subplt[row, col].pie([0])
                        warningmessage = (
                            "Issue displaying well "
                            + str(wellnum + 1)
                            + ". \n(possible zero value issue)"
                        )
                        C.messagebox.showwarning(
                            title="Warning", message=warningmessage
                        )
                        if C.globals_GC.debug:
                            C.globals_GC.mylog(e)
                elif datafilter.get() == 3:  # shade by yield
                    try:
                        # handle wells where one or more pie slices are zero
                        temp = totalcolormap.copy()
                        # iterate through list
                        mask = []
                        for idx, pievalue in enumerate(welldata):
                            # each time a zero is found, take index and remove corresponding color from temp of colormap
                            if float(pievalue) == 0:
                                mask = mask + [idx]
                        if len(mask) != 0:
                            temp = C.np.delete(temp, mask, 0)
                            welldata = [
                                val
                                for idx, val in enumerate(welldata)
                                if idx not in mask
                            ]
                        temp[int(self.shadebyyieldPopup.shadecol) - 1] = temp[
                            int(self.shadebyyieldPopup.shadecol) - 1
                        ] * (
                            welldata[int(self.shadebyyieldPopup.shadecol) - 1]
                            / excludeColmax
                        )
                        subplt[row, col].pie(
                            C.np.array(list(welldata) / min(list(welldata))),
                            colors=temp,
                            wedgeprops={"linewidth": 1, "edgecolor": [0, 0, 0]},
                            radius=1.3,
                            counterclock=False,
                        )
                    except Exception as e:
                        subplt[row, col].pie([0])
                        warningmessage = (
                            "Issue displaying well "
                            + str(wellnum + 1)
                            + ". \n(possible zero value issue)"
                        )
                        C.messagebox.showwarning(
                            title="Warning", message=warningmessage
                        )
                        if C.globals_GC.debug:
                            C.globals_GC.mylog(e)
                elif datafilter.get() == 4:  # group cutoffs
                    try:
                        # handle wells where one or more pie slices are zero
                        temp = totalcolormap.copy()
                        # iterate through list
                        mask = []
                        for idx, pievalue in enumerate(welldata):
                            # each time a zero is found, take index and remove corresponding color from temp of colormap
                            if float(pievalue) == 0:
                                mask = mask + [idx]
                        if len(mask) != 0:
                            temp = C.np.delete(temp, mask, 0)
                            welldata = [
                                val
                                for idx, val in enumerate(welldata)
                                if idx not in mask
                            ]
                        subplt[row, col].pie(
                            C.np.array(list(welldata) / min(list(welldata))),
                            colors=pickcolor(
                                totalcolormap.copy(),
                                int(self.numberofcutoffsPopup.cutoffcol) - 1,
                                cutoffvalues,
                                cutoffcolors,
                                welldata,
                            ),
                            wedgeprops={"linewidth": 1, "edgecolor": [0, 0, 0]},
                            radius=1.3,
                            counterclock=False,
                        )
                    except Exception as e:
                        subplt[row, col].pie([0])
                        warningmessage = (
                            "Issue displaying well "
                            + str(wellnum + 1)
                            + ". \n(possible zero value issue)"
                        )
                        C.messagebox.showwarning(
                            title="Warning", message=warningmessage
                        )
                        if C.globals_GC.debug:
                            C.globals_GC.mylog(e)
                else:
                    # handle wells where one or more pie slices are zero
                    temp = totalcolormap.copy()
                    # iterate through list
                    mask = []
                    for idx, pievalue in enumerate(welldata):
                        # each time a zero is found, take index and remove corresponding color from temp of colormap
                        if float(pievalue) == 0:
                            mask = mask + [idx]
                    if len(mask) != 0:
                        temp = C.np.delete(temp, mask, 0)
                        welldata = [
                            val for idx, val in enumerate(welldata) if idx not in mask
                        ]
                    subplt[row, col].pie(
                        C.np.array(list(welldata) / min(list(welldata))),
                        colors=temp,
                        wedgeprops={"linewidth": 1, "edgecolor": [0, 0, 0]},
                        radius=1.3,
                        counterclock=False,
                    )
                # write numbers accross the top
                if row == 0:
                    subplt[row, col].set_title(str(wellnum + 1))
                # write letters across the left side
                if col == 0:
                    subplt[row, col].set_ylabel(
                        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"][
                            row
                        ],
                        rotation=0,
                        labelpad=10,
                    )
            myfig.show()

        def pickcolor(colormap, cutoffcol, cutoffvalues, cutoffcolors, currentwell):
            for i in range(0, len(cutoffvalues) - 1):
                if (currentwell[cutoffcol] > cutoffvalues[i]) & (
                    currentwell[cutoffcol] <= cutoffvalues[i + 1]
                ):
                    colormap[cutoffcol] = cutoffcolors[i + 1]
                    return colormap
                elif currentwell[cutoffcol] <= cutoffvalues[i]:
                    colormap[cutoffcol] = cutoffcolors[i]
                    return colormap

        # Finish set up of user interface
        # make present data button
        C.tk.Button(self, text="Present", command=presentdatacallback).place(
            relx=0.4, rely=0.9
        )
        # make radio buttons for well layout
        layout = C.tk.IntVar()
        layouts = [("96 (8x12)", 1), ("96 (12x8)", 2), ("24 (4x6)", 3), ("24 (6x4)", 4)]
        C.tk.Label(self, text="Well layout:").place(x=5, y=40)
        yiterator = 60
        for i in range(len(layouts)):
            C.tk.Radiobutton(
                self,
                text=layouts[i][0],
                indicatoron=0,
                padx=10,
                variable=layout,
                value=layouts[i][1],
            ).place(x=5, y=yiterator)
            yiterator += 30

        # make radio buttons for graphic color
        colorscheme = C.tk.IntVar()
        colorschemes = [
            ("neutral", 1),
            ("bright", 2),
            ("deuteranomaly", 3),
            ("custom", 4),
        ]
        C.tk.Label(self, text="Color scheme:").place(x=130, y=40)
        yiterator = 60
        for i in range(len(colorschemes)):
            C.tk.Radiobutton(
                self,
                text=colorschemes[i][0],
                indicatoron=0,
                padx=8,
                variable=colorscheme,
                value=colorschemes[i][1],
            ).place(x=130, y=yiterator)
            yiterator += 30

        # make radio buttons for datafilters
        datafilter = C.tk.IntVar()
        datafilters = [
            ("none", 1),
            ("exclude threshold", 2),
            ("shade by yield", 3),
            ("set cutoffs", 4),
        ]
        C.tk.Label(self, text="Data filter:").place(x=255, y=40)
        yiterator = 60
        for i in range(len(datafilters)):
            C.tk.Radiobutton(
                self,
                text=datafilters[i][0],
                indicatoron=0,
                padx=10,
                variable=datafilter,
                value=datafilters[i][1],
            ).place(x=255, y=yiterator)
            yiterator += 30


class excludePopup(object):
    """
    Pop up which will ask the user which column they want to check
    and the value floor, for which wells below will not be displayed.

    Ex. Creating a selectivity chart, but not displaying wells where the
    yield is vanishingly small.
    """

    def __init__(self, master):
        top = self.top = C.tk.Toplevel(master)
        C.tk.Label(top, text="Column to filter by:").place(x=0, y=0)
        self.excludecol = C.tk.Entry(top)
        self.excludecol.place(x=0, y=25)
        C.tk.Label(top, text="Hide wells with values below:").place(x=0, y=50)
        self.excludeval = C.tk.Entry(top)
        self.excludeval.place(x=0, y=75)
        C.tk.Button(top, text="Ok", command=self.close).place(x=0, y=100)

    def close(self):
        self.excludecol = self.excludecol.get()
        self.excludeval = self.excludeval.get()
        self.top.destroy()


class shadebyyieldPopup(object):
    """
    Asks for which column to base the shading preference
    """

    def __init__(self, master):
        top = self.top = C.tk.Toplevel(master)
        C.tk.Label(top, text="Column to base shading on:").place(x=0, y=0)
        self.shadecol = C.tk.Entry(top)
        self.shadecol.place(x=0, y=25)
        C.tk.Button(top, text="Ok", command=self.close).place(x=0, y=50)

    def close(self):
        self.shadecol = self.shadecol.get()
        self.top.destroy()


class numberofcutoffsPopup(object):
    """
    Asks user for both the column to base the groupign on and
    the number of groups to generate
    """

    def __init__(self, master):
        top = self.top = C.tk.Toplevel(master)
        C.tk.Label(top, text="Number of groups:").place(x=0, y=0)
        self.numgroups = C.tk.Entry(top)
        self.numgroups.place(x=0, y=25)
        C.tk.Label(top, text="Column to base groups on:").place(x=0, y=50)
        self.cutoffcol = C.tk.Entry(top)
        self.cutoffcol.place(x=0, y=75)
        C.tk.Button(top, text="Ok", command=self.close).place(x=0, y=100)

    def close(self):
        self.numgroups = self.numgroups.get()
        self.cutoffcol = self.cutoffcol.get()
        self.top.destroy()


class cutoffPopup(object):
    """
    enable the user to make custom cutoff colors, useful for grouping wells
    by selectivity or yield
    """

    def __init__(self, master):
        top = self.top = C.tk.Toplevel(master)
        C.tk.Label(top, text="For wells below this value:").place(x=0, y=0)
        self.cutoffval = C.tk.Entry(top)
        self.cutoffval.place(x=0, y=25)
        C.tk.Label(top, text="Use this color:").place(x=0, y=50)
        self.cutoffcolor = C.tk.Entry(top)
        self.cutoffcolor.insert(C.tk.END, "255,255,255")
        self.cutoffcolor.place(x=0, y=75)
        C.tk.Button(top, text="Ok", command=self.close).place(x=0, y=100)

    def close(self):
        self.cutoffval = self.cutoffval.get()
        self.cutoffcolor = self.cutoffcolor.get()
        self.top.destroy()