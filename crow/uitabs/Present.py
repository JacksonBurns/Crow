import tkinter.colorchooser as cc
import numpy as np
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plot
from matplotlib.cbook import get_sample_data
import matplotlib.patheffects as pe

from crow.utils.logger import mylog
from crow.utils.popupwindows.cutoff import cutoffPopup
from crow.utils.popupwindows.exclude import excludePopup
from crow.utils.popupwindows.numberofcutoffs import numberofcutoffsPopup
from crow.utils.popupwindows.shadebyyield import shadebyyieldPopup


class Present(tk.Frame):
    """
    Tab of the GC window resposible for taking columns
    of processed data and generating pie charts of the results,
    including various filters and color schemes.
    """

    def __init__(self, name, crow_globals):
        self._img_filenames = []
        tk.Frame.__init__(self, width=47, height=450)

        # begin defintiion of callbacks, followed by user interface
        def presentdatacallback():
            """
            Upon clicking the present data button, validate input and
            then read state of UI buttons to determine settings.
            """
            # check for wrong type of data selected
            if ".xml" in str(crow_globals.datafiles):
                messagebox.showerror(
                    "Error!",
                    "Please select input data file (.csv)! (to convert excel to .csv, use File->Save As... and select .csv)",
                )
                return
            # please select data
            elif len(crow_globals.datafiles) == 0:
                messagebox.showerror(
                    "Error!", "Please select excel data file (.csv)!",
                )
                return
            # please select only one excel file at a time
            elif len(crow_globals.datafiles) != 1:
                messagebox.showerror(
                    "Error!", "Please select a single excel data file (.csv)!",
                )
                return
            # if passes all tests, present accordingly
            # pull data from user entered file

            exceldata = np.genfromtxt(
                crow_globals.datafiles[0], dtype=float, delimiter=",", names=True
            )
            if image_overlay.get():
                # the image filenames will have broken the input data
                self._img_filenames = []
                newdata = []
                for row in exceldata:
                    newrow = []
                    for value in row:
                        if not np.isnan(value):
                            newrow.append(value)
                    newdata.append(newrow)
                exceldata = newdata
                with open(crow_globals.datafiles[0], "r") as file:
                    for line in file.readlines()[1:]:
                        self._img_filenames.append(
                            line.split(",")[-1].replace("\n", "")
                        )

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
                    graphic_generator(
                        exceldata, [8, 12], totalcolormap, (6, 4))
                except Exception as e:
                    if crow_globals.debug:
                        mylog(e)
                    messagebox.showerror(
                        "Error - Try Again", e,
                    )
            # 96 (12x8)
            elif layout.get() == 2:
                try:
                    graphic_generator(
                        exceldata, [12, 8], totalcolormap, (4, 6))
                except Exception as e:
                    if crow_globals.debug:
                        mylog(e)
                    messagebox.showerror(
                        "Error - Try Again", e,
                    )
            # 24 (4x6)
            elif layout.get() == 3:
                try:
                    graphic_generator(exceldata, [4, 6], totalcolormap, (6, 4))
                except Exception as e:
                    if crow_globals.debug:
                        mylog(e)
                    messagebox.showerror(
                        "Error - Try Again", e,
                    )
            # 24 (6x4)
            elif layout.get() == 4:
                try:
                    graphic_generator(exceldata, [6, 4], totalcolormap, (4, 6))
                except Exception as e:
                    if crow_globals.debug:
                        mylog(e)
                    messagebox.showerror(
                        "Error - Try Again", e,
                    )
            # 48 (6x8)
            elif layout.get() == 5:
                try:
                    graphic_generator(exceldata, [6, 8], totalcolormap, (6, 4))
                except Exception as e:
                    if crow_globals.debug:
                        mylog(e)
                    messagebox.showerror(
                        "Error - Try Again", e,
                    )
            # 48 (8x6)
            elif layout.get() == 6:
                try:
                    graphic_generator(exceldata, [8, 6], totalcolormap, (4, 6))
                except Exception as e:
                    if crow_globals.debug:
                        mylog(e)
                    messagebox.showerror(
                        "Error - Try Again", e,
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
            messagebox.showwarning(title="Warning", message=warningmessage)
            if crow_globals.debug:
                mylog(e)

        def draw_filled(
            totalcolormap,
            welldata,
            subplt,
            row,
            col,
            datafilter=0,
            cutoffvalues=None,
            cutoffcolors=None,
            excludeColmax=None,
        ):
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
                welldata = [val for idx, val in enumerate(
                    welldata) if idx not in mask]
            if datafilter == 3:
                temp[int(self.shadebyyieldPopup.shadecol) - 1] = temp[
                    int(self.shadebyyieldPopup.shadecol) - 1
                ] * (welldata[int(self.shadebyyieldPopup.shadecol) - 1] / excludeColmax)
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
                    radius=1,
                    counterclock=False,
                )
            else:
                subplt[row, col].pie(
                    np.array(list(welldata) / min(list(welldata))),
                    colors=temp,
                    wedgeprops={"linewidth": 1, "edgecolor": [0, 0, 0]},
                    radius=1,
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
                    cutoffvalues = cutoffvalues + \
                        [float(self.cutoffPopup.cutoffval)]
                    cutoffcolors = cutoffcolors + [
                        [int(s) / 255 for s in self.cutoffPopup.cutoffcolor.split(",")]
                    ]
            # create figure with correct number of subplots
            if image_overlay.get():
                myfig, subplt = plot.subplots(
                    subplotdims[0],
                    subplotdims[1] * 2,
                    figsize=(dims[1] * 2 * 12, dims[0] * 10),
                    dpi=200,
                )
            else:
                myfig, subplt = plot.subplots(
                    subplotdims[0], subplotdims[1], figsize=dims
                )
            for wellnum in range(0, subplotdims[0] * subplotdims[1]):
                # go to position
                row = wellnum // subplotdims[1]
                col = wellnum % subplotdims[1]
                if image_overlay.get():
                    col *= 2
                # well data
                welldata = exceldata[wellnum]
                if datafilter.get() == 2:  # exclude threshold
                    try:
                        if welldata[int(self.excludePopup.excludecol) - 1] < float(
                            self.excludePopup.excludeval
                        ):  # exclude cutoff
                            subplt[row, col].pie([0])
                        else:
                            draw_filled(totalcolormap, welldata,
                                        subplt, row, col)
                    except Exception as e:
                        draw_empty(subplt, row, col, wellnum, e)
                elif datafilter.get() == 3:  # shade by yield
                    try:
                        draw_filled(
                            totalcolormap,
                            welldata,
                            subplt,
                            row,
                            col,
                            datafilter=datafilter.get(),
                            excludeColmax=excludeColmax,
                        )
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
                    im = plot.imread(get_sample_data(
                        self._img_filenames[wellnum]))
                    subplt[row, col + 1].imshow(im)
                    subplt[row, col + 1].axis("off")

            # write a legend for the colors
            with open(crow_globals.datafiles[0], "r") as file:
                count = 0
                headers = file.readline().split(",")
                if image_overlay.get():
                    end = len(headers) - 1
                else:
                    end = len(headers)
                for header in headers[:end]:
                    myfig.text(
                        0.2 + 0.1 * count,
                        0.98,
                        header.replace("\n", ""),
                        ha="center",
                        va="bottom",
                        size=70,
                        color=totalcolormap[count],
                        path_effects=[pe.withStroke(
                            linewidth=1, foreground='black')],
                    )
                    count += 1
            plot.tight_layout()
            if write_to_file.get():
                fname = (
                    "CrowHTE_present_output_" +
                    time.strftime("%Y%m%d-%H%M%S") + ".png"
                )
                myfig.savefig(
                    fname, bbox_inches="tight", pad_inches=0.01, dpi=myfig.dpi,
                )
                messagebox.showinfo(
                    "Graphic Generation Complete",
                    "Successfully wrote ouput to " + fname,
                )
                webbrowser.open(fname)
            else:
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
        tk.Checkbutton(
            self,
            text="Last column contains image filepaths",
            variable=image_overlay,
            onvalue=True,
            offvalue=False,
            height=1,
            width=30,
        ).place(relx=0.3, rely=0.8)

        # make check button for writing image to file
        write_to_file = tk.IntVar()
        tk.Checkbutton(
            self,
            text="Save graphic directly to file",
            variable=write_to_file,
            onvalue=True,
            offvalue=False,
            height=1,
            width=30,
        ).place(relx=0.3, rely=0.75)

        # make radio buttons for well layout
        layout = tk.IntVar()
        layouts = [("96 (8x12)", 1), ("96 (12x8)", 2),
                   ("24 (4x6)", 3), ("24 (6x4)", 4),
                   ("48 (6x8)", 5), ("48 (8x6)", 6), ]
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
