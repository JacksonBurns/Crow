# -*- coding: utf-8 -*-
# This is the wrapper function for Crow - GC
import glob
import webbrowser
import pkg_resources
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plot
from matplotlib.cbook import get_sample_data
from mpl_toolkits.axes_grid.inset_locator import inset_axes

import numpy as np
import tkinter.colorchooser as cc

# retrieve functions written elsewhere
from Crow.helper_functions import ParseXML, RequestFiles

# retreive global datafiles list variable
from Crow.Crow_GC import globals_GC


# define GUI
class Crow_GC(tk.Frame):
    """
    Parent window for the GC app, which contains the global variables
    including raw data and input data, as well as holding the notebook
    which containts the 3 tabs (PrePull, Pull, Present)

    """

    def __init__(self, master):
        globals_GC.init()
        # create base window, name it, and size it
        self.master = master
        master.title("Crow - GC")
        master.geometry("800x500")
        # set up 3 tabs
        tk.Frame.__init__(self)
        self.notebook = ttk.Notebook()
        self.notebook.add(PrePull(self.notebook), text="Pre-Pull")
        self.notebook.add(Pull(self.notebook), text="Pull")
        self.notebook.add(Present(self.notebook), text="Present")
        self.notebook.place(x=0, y=0)
        # add data selector
        self.FileDisplay = tk.StringVar()
        self.FileDisplay = ""

        # define select data callback function
        def selectrawdatacallback():
            """
            Upon clicking the select data button, open up a file request window
            and set the currently selected files to those which are selected,
            update the display
            """
            globals_GC.datafiles = RequestFiles.RequestFiles(
                "Raw Data", "*.xml", globals_GC.rawdatapath
            )
            self.FileDisplay = (
                str(globals_GC.datafiles)
                .replace(",", "\n")
                .replace("(", "")
                .replace(")", "")
            )
            update_files()

        # define excel data callback
        def selectexceldatacallback():
            """
            Create pop-up file request for ".csv" input data for present
            """
            globals_GC.datafiles = RequestFiles.RequestFiles(
                "Processed Data", "*.csv", globals_GC.exportdatapath
            )
            self.FileDisplay = (
                str(globals_GC.datafiles)
                .replace(",", "\n")
                .replace("(", "")
                .replace(")", "")
            )
            update_files()

        # data files display
        def update_files():
            """
            Counts the total number of files selected (useful for large experiments)
            and concatenates to the beggining of the list of file names.
            """
            temp = tk.Text(master, height=10, width=35)
            temp.insert(
                tk.END,
                str(len(globals_GC.datafiles)) + " TOTAL FILES\n" + self.FileDisplay,
            )
            temp.place(x=470, y=65)
            temp.config(state="disabled")

        update_files()
        # data files label
        tk.Label(master, text="Current Data Files:").place(x=470, y=40)
        # Select Data files button
        tk.Button(master, text="Select Raw Data", command=selectrawdatacallback).place(
            x=470, y=245
        )
        # Select Data files button
        tk.Button(
            master, text="Select Excel Data", command=selectexceldatacallback
        ).place(x=650, y=245)

        # Retrieve files from server by experiment name
        def searchservercallback():
            """
            Go to given 'server' location and glob for any file matching
            the given experiment name
            """
            globals_GC.datafiles = glob.glob(
                globals_GC.rawdatapath + "*" + self.expname.get() + "*"
            )
            self.FileDisplay = (
                str(globals_GC.datafiles)
                .replace(",", "\n")
                .replace("[", "")
                .replace("]", "")
            )
            update_files()

        def openconfigcallback():
            webbrowser.open(pkg_resources.resource_filename(__name__, "config.yaml"))

        tk.Button(
            master, text="Open Config. File", command=openconfigcallback
        ).place(x=470, y=340)

        tk.Button(
            master, text="Search Server by Expt. Name", command=searchservercallback
        ).place(x=470, y=310)
        self.expname = tk.Entry(master)
        self.expname.place(x=470, y=280)
        # title on top of window
        tk.Label(master, text="Crow Really Outta Work").place(relx=0.78, y=0)
        # setup callback for closing app
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)

    def close_app(self):
        """
        Adds a pop-up message to ensure that the user actually intended to quit,
        then on confirmation destorys the app so that the parent GUI
        can be launched again.
        """
        if messagebox.askokcancel(title="Quit", message="Are you sure?"):
            sys.exit(0)


class PrePull(tk.Frame):
    """
    Tab which contains functionality of pre-pulling, which involves
    parsing all entered data files and creating a histogram
    """

    def __init__(self, name):
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
            if len(globals_GC.datafiles) == 0:
                messagebox.showerror("Error!", "No .xml data files selected.")
            elif ".xlsx" in str(globals_GC.datafiles):
                messagebox.showerror(
                    "Error!", "Please select raw data files, not processed excel data!"
                )
            else:
                # iterate through each and pull relevant data
                self.datadict = {}
                for file in globals_GC.datafiles:
                    try:
                        temp = ParseXML.ParseXML(file)
                        temp = temp[globals_GC.peaktarg[0]][globals_GC.peaktarg[1]]
                        for peak in temp[1:]:
                            rettime = round(float(peak[globals_GC.rettarg].text), 2)
                            if rettime in self.datadict:
                                self.datadict[rettime] += 1
                            else:
                                self.datadict[rettime] = 1
                    except Exception as e:
                        if globals_GC.debug:
                            globals_GC.mylog(e)
                        warningmessage = (
                            "No peak data found in file "
                            + str(file)
                            + "\n (possible failed injection)"
                        )
                        messagebox.showwarning(
                            title="Warning", message=warningmessage
                        )
                # display the histogram
                plot.bar(
                    list(self.datadict.keys()),
                    list(self.datadict.values()),
                    width=globals_GC.roundres,
                )
                plot.ylabel("Number of Wells")
                plot.xlabel("Retention Time (minutes)")
                plot.show()

        # Pre-Pull button
        tk.Button(self, text="Generate Histogram", command=prepullcallback).place(
            relx=0.3, rely=0.35
        )


class Present(tk.Frame):
    """
    Tab of the GC window resposible for taking columns
    of processed data and generating pie charts of the results,
    including various filters and color schemes.
    """

    def __init__(self, name):
        self._img_filenames = []
        tk.Frame.__init__(self, width=47, height=450)

        # begin defintiion of callbacks, followed by user interface
        def presentdatacallback():
            """
            Upon clicking the present data button, validate input and
            then read state of UI buttons to determine settings.
            """
            # check for wrong type of data selected
            if ".xml" in str(globals_GC.datafiles):
                messagebox.showerror(
                    "Error!", "Please select input data file (.csv)! (to convert excel to .csv, use File->Save As... and select .csv)",
                )
                return
            # please select data
            elif len(globals_GC.datafiles) == 0:
                messagebox.showerror(
                    "Error!", "Please select excel data file (.csv)!",
                )
                return
            # please select only one excel file at a time
            elif len(globals_GC.datafiles) != 1:
                messagebox.showerror(
                    "Error!", "Please select a single excel data file (.csv)!",
                )
                return
            # if passes all tests, present accordingly
            # pull data from user entered file
            
            exceldata = np.genfromtxt(
                globals_GC.datafiles[0], dtype=float, delimiter=",", names=True
            )
            if image_overlay.get():
                # the image filenames will have broken the input data
                newdata = []
                for row in exceldata:
                    newrow = []
                    for value in row:
                        if not np.isnan(value):
                            newrow.append(value)
                    newdata.append(newrow)
                exceldata = newdata
                with open(globals_GC.datafiles[0], "r") as file:
                    for line in file.readlines()[1:]:
                        self._img_filenames.append(line.split(",")[-1].replace("\n",""))

            # check for files that are too big
            if len(exceldata[0]) > 9:
                messagebox.showerror(
                    "Error!", "Data has too many columns (>10).",
                )
            # decide on colorscheme from color radio buttons
            if colorscheme.get() == 1:  # neutral
                totalcolormap = np.array(
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
                totalcolormap = np.array(
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
                totalcolormap = np.array(
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
                    rgb, _ = cc.askcolor(
                        parent=self, title="Choose color " + str(i + 1)
                    )
                    totalcolormap = totalcolormap + [np.array(list(rgb)) / 256]
            else:
                messagebox.showerror(
                    "Error!", "Please select a color scheme!",
                )
                return
            # call graphic generator appropriately
            # 96 (8x12)
            if layout.get() == 1:
                try:
                    graphic_generator(exceldata, [8, 12], totalcolormap, (6, 4))
                except Exception as e:
                    if globals_GC.debug:
                        globals_GC.mylog(e)
                    messagebox.showerror(
                        "Error!", "Something went wrong, please try again.",
                    )
            # 96 (12x8)
            elif layout.get() == 2:
                try:
                    graphic_generator(exceldata, [12, 8], totalcolormap, (4, 6))
                except Exception as e:
                    if globals_GC.debug:
                        globals_GC.mylog(e)
                    messagebox.showerror(
                        "Error!", "Something went wrong, please try again.",
                    )
            # 24 (4x6)
            elif layout.get() == 3:
                # try:
                graphic_generator(exceldata, [4, 6], totalcolormap, (6, 4))
                # except Exception as e:
                #     if globals_GC.debug:
                #         globals_GC.mylog(e)
                #     messagebox.showerror(
                #         "Error!", "Something went wrong, please try again.",
                #     )
            # 24 (6x4)
            elif layout.get() == 4:
                try:
                    graphic_generator(exceldata, [6, 4], totalcolormap, (4, 6))
                except Exception as e:
                    if globals_GC.debug:
                        globals_GC.mylog(e)
                    messagebox.showerror(
                        "Error!", "Something went wrong, please try again.",
                    )
            else:
                messagebox.showerror("Error!", "Please select a layout.")

        def draw_empty(subplt, row, col, wellnum, e):
            subplt[row, col].pie([0])
            warningmessage = (
                "Issue displaying well "
                + str(wellnum + 1)
                + ". \n(possible zero value issue)"
            )
            messagebox.showwarning(
                title="Warning", message=warningmessage
            )
            if globals_GC.debug:
                globals_GC.mylog(e)

        def draw_filled(totalcolormap, welldata, subplt, row, col, datafilter=0, cutoffvalues=None, cutoffcolors=None, excludeColmax=None):
            # handle wells where one or more pie slices are zero
            temp = totalcolormap.copy()
            # iterate through list
            mask = []
            for idx, pievalue in enumerate(welldata):
                # each time a zero is found, take index and remove corresponding color from temp of colormap
                if float(pievalue) == 0:
                    mask = mask + [idx]
            if len(mask) != 0:
                temp = np.delete(temp, mask, 0)
                welldata = [
                    val for idx, val in enumerate(welldata) if idx not in mask
                ]
            if datafilter == 3:
                temp[int(self.shadebyyieldPopup.shadecol) - 1] = temp[
                    int(self.shadebyyieldPopup.shadecol) - 1
                ] * (
                    welldata[int(self.shadebyyieldPopup.shadecol) - 1]
                    / excludeColmax
                )
            if datafilter == 4:
                subplt[row, col].pie(
                    np.array(list(welldata) / min(list(welldata))),
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
            else:
                subplt[row, col].pie(
                    np.array(list(welldata) / min(list(welldata))),
                    colors=temp,
                    wedgeprops={"linewidth": 1, "edgecolor": [0, 0, 0]},
                    radius=1.3,
                    counterclock=False,
                )

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
                # popup to ask which column the gradient should be based off of is in
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
            myfig, subplt = plot.subplots(
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
                            draw_filled(totalcolormap, welldata, subplt, row, col)
                    except Exception as e:
                        draw_empty(subplt, row, col, wellnum, e)
                elif datafilter.get() == 3:  # shade by yield
                    try:
                        draw_filled(totalcolormap, welldata, subplt, row, col, datafilter=datafilter.get(), excludeColmax=excludeColmax)
                    except Exception as e:
                        draw_empty(subplt, row, col, wellnum, e)
                elif datafilter.get() == 4:  # group cutoffs
                    try:
                        draw_filled(
                            totalcolormap,
                            welldata,
                            subplt,
                            row,
                            col,
                            datafilter=datafilter.get(),
                            cutoffvalues=cutoffvalues,
                            cutoffcolors=cutoffcolors,
                            )
                    except Exception as e:
                        draw_empty(subplt, row, col, wellnum, e)
                else:
                    draw_filled(totalcolormap, welldata, subplt, row, col)
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
                # draw the image over the well
                if image_overlay.get():
                    im = plot.imread(get_sample_data(self._img_filenames[wellnum]))
                    if layout.get() == 1:
                        ax = myfig.add_axes([0.09 + 0.8 * col / subplotdims[1], 0.8 - 0.8 * row / subplotdims[0], 1 / subplotdims[0], 1 / subplotdims[1]])
                    elif layout.get() == 2:
                        ax = myfig.add_axes([0.12 + 0.8 * col / subplotdims[1], 0.78 - 0.772 * row / subplotdims[0], 1 / subplotdims[0], 1 / subplotdims[1]])
                    elif layout.get() == 3:
                        ax = myfig.add_axes([0.06 + 0.8 * col / subplotdims[1], 0.7 - 0.8 * row / subplotdims[0], 1 / subplotdims[0], 1 / subplotdims[1]])
                    elif layout.get() == 4:
                        ax = myfig.add_axes([0.14 + 0.8 * col / subplotdims[1], 0.7 - 0.8 * row / subplotdims[0], 1 / subplotdims[0], 1 / subplotdims[1]])
                    else:
                        continue
                    ax.imshow(im)
                    ax.axis('off')

                    # subplt[row, col + 1].imshow(im)
                    # subplt[row, col + 1].axis("off")

            # write a legend for the colors
            with open(globals_GC.datafiles[0], "r") as file:
                count = 0
                headers = file.readline().split(",")
                if image_overlay.get():
                    end = len(headers) - 1
                else:
                    end = len(headers)
                for header in headers[:end]:
                    myfig.text(0.2 + 0.1 * count, 0.95, header.replace("\n",""), ha="center", va="bottom", size="medium", color=totalcolormap[count])
                    count += 1
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
        tk.Button(self, text="Present", command=presentdatacallback).place(
            relx=0.4, rely=0.9
        )

        # make check button for image overlay
        image_overlay = tk.IntVar()
        tk.Checkbutton(self, text = "Last column contains image filepaths", variable = image_overlay,
                onvalue = True, offvalue = False, height=1,
                width = 30).place(relx=0.3, rely=0.8)

        # make radio buttons for well layout
        layout = tk.IntVar()
        layouts = [("96 (8x12)", 1), ("96 (12x8)", 2), ("24 (4x6)", 3), ("24 (6x4)", 4)]
        tk.Label(self, text="Well layout:").place(x=5, y=40)
        yiterator = 60
        for i in range(len(layouts)):
            tk.Radiobutton(
                self,
                text=layouts[i][0],
                indicatoron=0,
                padx=10,
                variable=layout,
                value=layouts[i][1],
            ).place(x=5, y=yiterator)
            yiterator += 30

        # make radio buttons for graphic color
        colorscheme = tk.IntVar()
        colorschemes = [
            ("neutral", 1),
            ("bright", 2),
            ("deuteranomaly", 3),
            ("custom", 4),
        ]
        tk.Label(self, text="Color scheme:").place(x=130, y=40)
        yiterator = 60
        for i in range(len(colorschemes)):
            tk.Radiobutton(
                self,
                text=colorschemes[i][0],
                indicatoron=0,
                padx=8,
                variable=colorscheme,
                value=colorschemes[i][1],
            ).place(x=130, y=yiterator)
            yiterator += 30

        # make radio buttons for datafilters
        datafilter = tk.IntVar()
        datafilters = [
            ("none", 1),
            ("exclude threshold", 2),
            ("shade by yield", 3),
            ("set cutoffs", 4),
        ]
        tk.Label(self, text="Data filter:").place(x=255, y=40)
        yiterator = 60
        for i in range(len(datafilters)):
            tk.Radiobutton(
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
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="Column to filter by:").place(x=0, y=0)
        self.excludecol = tk.Entry(top)
        self.excludecol.place(x=0, y=25)
        tk.Label(top, text="Hide wells with values below:").place(x=0, y=50)
        self.excludeval = tk.Entry(top)
        self.excludeval.place(x=0, y=75)
        tk.Button(top, text="Ok", command=self.close).place(x=0, y=100)

    def close(self):
        self.excludecol = self.excludecol.get()
        self.excludeval = self.excludeval.get()
        self.top.destroy()


class shadebyyieldPopup(object):
    """
    Asks for which column to base the shading preference
    """

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="Column to base shading on:").place(x=0, y=0)
        self.shadecol = tk.Entry(top)
        self.shadecol.place(x=0, y=25)
        tk.Button(top, text="Ok", command=self.close).place(x=0, y=50)

    def close(self):
        self.shadecol = self.shadecol.get()
        self.top.destroy()


class numberofcutoffsPopup(object):
    """
    Asks user for both the column to base the groupign on and
    the number of groups to generate
    """

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="Number of groups:").place(x=0, y=0)
        self.numgroups = tk.Entry(top)
        self.numgroups.place(x=0, y=25)
        tk.Label(top, text="Column to base groups on:").place(x=0, y=50)
        self.cutoffcol = tk.Entry(top)
        self.cutoffcol.place(x=0, y=75)
        tk.Button(top, text="Ok", command=self.close).place(x=0, y=100)

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
        top = self.top = tk.Toplevel(master)
        tk.Label(top, text="For wells below this value:").place(x=0, y=0)
        self.cutoffval = tk.Entry(top)
        self.cutoffval.place(x=0, y=25)
        tk.Label(top, text="Use this color:").place(x=0, y=50)
        self.cutoffcolor = tk.Entry(top)
        self.cutoffcolor.insert(tk.END, "255,255,255")
        self.cutoffcolor.place(x=0, y=75)
        tk.Button(top, text="Ok", command=self.close).place(x=0, y=100)

    def close(self):
        self.cutoffval = self.cutoffval.get()
        self.cutoffcolor = self.cutoffcolor.get()
        self.top.destroy()


class Pull(tk.Frame):
    """
    Tab of the GC window responsible for pulling data from the entered
    xml files based on the indicated retention times and variability
    """

    def __init__(self, name):
        tk.Frame.__init__(self, width=47, height=450)
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
            if ".xlsx" in str(globals_GC.datafiles):
                messagebox.showerror("Error!", "Please select raw data files.")
                return
            # check for missing tols or rt
            elif (len(self.rettimes) != len(self.toltimes)) or (
                len(self.rettimes) == 0 or len(self.toltimes) == 0
            ):
                tk.messagebox.showerror(
                    "Error!E", "At least one retention time/tolerance is missing."
                )
                return
            # break if non-chronological
            elif sorted(self.rettimes) != self.rettimes:
                tk.messagebox.showerror(
                    "Error!", "Retention times are not in chronological order.",
                )
                return
            # break if there is overlap in entered values also
            elif self.isthereoverlap():
                return
            elif len(globals_GC.datafiles) == 0:
                messagebox.showerror("Error!", "No raw data files selected.")
                return
            # after passing all validation, continue to remainder of method.
            # iterate through each and pull relevant data
            self.datalist = np.empty(  # empty array the size of len(datafile) x number of products
                [len(globals_GC.datafiles)-1, len(self.rettimes)], dtype=object
            )
            # iterate through each data test
            for file in globals_GC.datafiles:
                try:
                    # open file
                    temp = ParseXML.ParseXML(file)
                    # go to where peaks are stored
                    peaks = temp[globals_GC.peaktarg[0]][globals_GC.peaktarg[1]]
                    # setup a pair of lists to store information for
                    # peaks which fall within the window
                    peaksinwindow = []
                    # iterate through all the peaks
                    for peak in peaks[1:]:
                        # check if the peaks are the one we want
                        for i in range(0, len(self.rettimes)):
                            if (  # retention time - tolerance < limit
                                (
                                    float(peak[globals_GC.rettarg].text)
                                    - self.toltimes[i]
                                )
                                < self.rettimes[i]
                            ) & (  # retention time + tolerance > limit
                                (
                                    float(peak[globals_GC.rettarg].text)
                                    + self.toltimes[i]
                                )
                                > self.rettimes[i]
                            ):
                                # every time a valid peak is found, append its
                                # retention time and area to this list
                                peaksinwindow.append(
                                    tuple(
                                        [
                                            float(peak[globals_GC.rettarg].text),
                                            float(peak[globals_GC.areatarg].text),
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
                    if globals_GC.debug:
                        globals_GC.mylog(ie)
                    warningmessage = (
                        "Please select files in order starting from 1 to end"
                    )
                    messagebox.showwarning(title="Warning", message=warningmessage)
                except Exception as e:
                    if globals_GC.debug:
                        globals_GC.mylog(e)
                    warningmessage = (
                        "No peak data found in file "
                        + str(file)
                        + "\n (possible failed injection)"
                    )
                    messagebox.showwarning(title="Warning", message=warningmessage)
            with open(globals_GC.exportdatapath + self.expname.get() + ".csv", "w") as file:
                # write header
                for i in range(len(self.rettimes)):
                    file.write("eluate "+str(i+1)+"\t")
                file.write("\n")
                # write all lines to a file in a tab separated value format
                for row in self.datalist:
                    for entry in row:
                        file.write(entry+"\t")
                    file.write("\n")
            msg = "Data successfully written to " + globals_GC.exportdatapath + self.expname.get() + ".csv"
            messagebox.showinfo(title="Data Written", message=msg)

        # pull data button
        tk.Button(self, text="Pull Requested Data", command=pulldatacallback).place(
            x=145, y=415
        )
        # set up button for picking method
        self.pickingmethod = tk.IntVar()
        methods = [("Keep Centermost", 1), ("Keep Maximum", 2), ("Keep All", 3)]
        tk.Label(self, text="Peak picking method:").place(x=150, y=305)
        yiterator = 325
        for i in range(len(methods)):
            tk.Radiobutton(
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
        self.retinclude = tk.IntVar()
        tk.Checkbutton(
            self,
            text='Include retention times?',
            variable=self.retinclude,
            onvalue=1,
            offvalue=0).place(
                x=280,
                y=415)

        # clear entries button
        tk.Button(self, text="Clear Entries", command=clearentriescallback).place(
            x=167, y=245
        )
        # Experiment Name Label
        tk.Label(self, text="Expt. Name:").place(x=85, y=280)
        # Experiment Name Entry Field
        self.expname = tk.Entry(self)
        self.expname.place(x=170, y=280)

        def add_entry_fields():
            tk.Label(self, text="Retention Time (minutes)").place(x=40, y=40)
            # assigning and placing have to be on seperate lines because place returns nothing
            self.rt1 = tk.Entry(self)
            self.rt1.place(x=40, y=65)
            self.rt2 = tk.Entry(self)
            self.rt2.place(x=40, y=90)
            self.rt3 = tk.Entry(self)
            self.rt3.place(x=40, y=115)
            self.rt4 = tk.Entry(self)
            self.rt4.place(x=40, y=140)
            self.rt5 = tk.Entry(self)
            self.rt5.place(x=40, y=165)
            self.rt6 = tk.Entry(self)
            self.rt6.place(x=40, y=190)
            self.rt7 = tk.Entry(self)
            self.rt7.place(x=40, y=215)
            # define tolerance entry fields
            tk.Label(self, text="Tolerance Time (minutes)").place(x=230, y=40)
            self.tol1 = tk.Entry(self)
            self.tol1.place(x=230, y=65)
            self.tol2 = tk.Entry(self)
            self.tol2.place(x=230, y=90)
            self.tol3 = tk.Entry(self)
            self.tol3.place(x=230, y=115)
            self.tol4 = tk.Entry(self)
            self.tol4.place(x=230, y=140)
            self.tol5 = tk.Entry(self)
            self.tol5.place(x=230, y=165)
            self.tol6 = tk.Entry(self)
            self.tol6.place(x=230, y=190)
            self.tol7 = tk.Entry(self)
            self.tol7.place(x=230, y=215)

        # define retention time fields and label
        add_entry_fields()

    def entryreadorclear(self, readorclear):
        if readorclear == "clear":
            self.rt1.delete(0, tk.END)
            self.tol1.delete(0, tk.END)
            self.rt2.delete(0, tk.END)
            self.tol2.delete(0, tk.END)
            self.rt3.delete(0, tk.END)
            self.tol3.delete(0, tk.END)
            self.rt4.delete(0, tk.END)
            self.tol4.delete(0, tk.END)
            self.rt5.delete(0, tk.END)
            self.tol5.delete(0, tk.END)
            self.rt6.delete(0, tk.END)
            self.tol6.delete(0, tk.END)
            self.rt7.delete(0, tk.END)
            self.tol7.delete(0, tk.END)
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
                if globals_GC.debug:
                    globals_GC.mylog(e)
                messagebox.showerror(
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
                    tk.messagebox.showerror(
                        "Error!",
                        "Retention time/tolerance "
                        + str(i)
                        + " overlaps "
                        + str(i + 1)
                        + ".",
                    )
                    return True
