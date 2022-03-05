""" Test the methods of Crow."""
import os
import contextlib
import tkinter
import unittest
from unittest.mock import patch

from crow.Crow import main, CrowBase
from crow.utils.crow_globals import crow_globals
from crow.utils.logger import mylog
from crow.utils.ParseXML import ParseXML
from crow.utils.RequestFiles import RequestFiles
from crow.utils.popupwindows.cutoff import cutoffPopup
from crow.utils.popupwindows.exclude import excludePopup
from crow.utils.popupwindows.numberofcutoffs import numberofcutoffsPopup
from crow.utils.popupwindows.shadebyyield import shadebyyieldPopup
from crow.uitabs.PrePull import PrePull
from crow.uitabs.Pull import Pull
from crow.uitabs.Present import Present


class TestCrow(unittest.TestCase):
    """
    Test the various functionalities of Crow.
    """

    def test_CrowBase(self):
        """
        Running Crow base GUI with patched out tk calls.
        """
        with patch("crow.Crow.tk.Tk.mainloop") as test_gui:
            main()
            self.assertTrue(test_gui.called)

        master = tkinter.Tk()
        cb = CrowBase(master)

        with patch("crow.Crow.RequestFiles.RequestFiles") as test_request:
            cb.selectprocesseddata.invoke()
            self.assertTrue(test_request.called)

        with patch("crow.Crow.RequestFiles.RequestFiles") as test_request:
            cb.selectrawdatabutton.invoke()
            self.assertTrue(test_request.called)

        with patch("crow.Crow.glob.glob") as test_search:
            cb.searchserverbutton.invoke()
            self.assertTrue(test_search.called)

        with patch("crow.Crow.webbrowser.open") as test_open:
            cb.openconfigbutton.invoke()
            self.assertTrue(test_open.called)

        with patch("crow.Crow.messagebox.askokcancel") as test_confirm:
            with patch("crow.Crow.sys.exit") as test_exit:
                cb.close_app()
                self.assertTrue(test_confirm.called)
                self.assertTrue(test_exit.called)

    def test_crow_globals(self):
        """
        Initialization of variables used in all tabs of crow
        """
        with open("test-config.yaml", "w") as file:
            file.writelines([
                "config:\n",
                "    server_data_location: Z:\\test\\server_data\\\n",
                "    debug: True\n",
                "    export_data_path: Z:\\test\\export_data\\\n",
                "    pre_pull_rounding_resolution: 0.0025\n",
                "    xml_peaks_target: [8, 6]\n",
                "    xml_retention_time_target: 9\n",
                "    xml_area_target: 15\n",
                "    xml_wellnum_target: [1, 12]\n"])
        cg = crow_globals(config="test-config.yaml")
        self.assertEqual(cg.datafiles, [])
        self.assertTrue(cg.debug)
        self.assertEqual(cg.rawdatapath, "Z:\\test\\server_data\\")
        self.assertEqual(cg.exportdatapath, "Z:\\test\\export_data\\")
        self.assertEqual(cg.peaktarg, [8, 6])
        self.assertEqual(cg.rettarg, 9)
        self.assertEqual(cg.areatarg, 15)
        self.assertEqual(cg.roundres, 0.0025)
        self.assertEqual(cg.welltarg, [1, 12])
        os.remove("test-config.yaml")

    def test_mylog(self):
        """
        Debug logger used by all parts of Crow.
        """
        try:
            # intentionally cause an exception
            3 / 0
        except Exception as e:
            mylog(e)
        self.assertTrue(os.path.isfile("debug.txt"))
        # remove file to prevent cluttering
        os.remove("debug.txt")

    def test_ParseXML(self):
        """
        File reading capability used in Crow.
        """
        with open("temp.xml", "w") as file:
            file.writelines([
                "<Module>\n",
                "    <Number>1</Number>\n",
                "    <NumberInModule>1</NumberInModule>\n",
                "    <ModuleName>Agilent 6890 GC</ModuleName>\n",
                "    <SerialNumber>US00041800</SerialNumber>\n",
                "    <FirmwareRevision>A.03.08</FirmwareRevision>\n",
                "    <PartNumber>6890</PartNumber>\n",
                "</Module>"])
        root_test = ParseXML("temp.xml")
        # check various parts of the returned root to ensure that it is read correctly
        self.assertEqual(root_test[0].text, "1")
        self.assertEqual(root_test[2].text, "Agilent 6890 GC")
        self.assertEqual(root_test[5].text, "6890")
        # remove temporary file
        os.remove("temp.xml")

    def test_RequestFiles(self):
        """
        Launch the file request UI
        """
        with patch("crow.utils.RequestFiles.filedialog.askopenfilenames") as test_filereq:
            RequestFiles("Test Desccription", ".txt", ".")
            self.assertTrue(test_filereq.called)

    def test_PrePull(self):
        """
        Various cases for the PrePull tab
        """
        prepull = PrePull("test prepull", crow_globals())
        with patch("crow.uitabs.PrePull.messagebox.showerror") as test_missingxml:
            prepull.prepullbutton.invoke()
            self.assertTrue(test_missingxml.called)

        cg = crow_globals()
        cg.datafiles = ['test.csv']
        prepull = PrePull("test prepull", cg)
        with patch("crow.uitabs.PrePull.messagebox.showerror") as test_missingxml:
            prepull.prepullbutton.invoke()
            self.assertTrue(test_missingxml.called)

        cg = crow_globals()
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
        ]
        prepull = PrePull("test prepull", cg)
        with patch("crow.uitabs.PrePull.plot.show") as test_plot:
            prepull.prepullbutton.invoke()
            self.assertTrue(test_plot.called)

        open("blank.xml", "w").close()
        cg = crow_globals()
        cg.datafiles = ["blank.xml"]
        cg.debug = True
        prepull = PrePull("test prepull", cg)
        with patch("crow.uitabs.PrePull.mylog") as test_debug:
            with patch("crow.uitabs.PrePull.messagebox.showwarning") as test_warning:
                with patch("crow.uitabs.PrePull.plot.show") as test_plot:
                    prepull.prepullbutton.invoke()
                    self.assertTrue(test_plot.called)
                    self.assertTrue(test_debug.called)
                    self.assertTrue(test_warning.called)
        os.remove("blank.xml")

    def test_Pull(self):
        """
        Pull methods and callbacks.
        """
        # succcessful operation
        cg = crow_globals()
        cg.debug = True
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
        ]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "2")
        pull.tol2.insert(0, "0.1")
        pull.rt3.insert(0, "3")
        pull.tol3.insert(0, "0.1")
        pull.rt4.insert(0, "4")
        pull.tol4.insert(0, "0.1")
        pull.rt5.insert(0, "5")
        pull.tol5.insert(0, "0.1")
        pull.rt6.insert(0, "6")
        pull.tol6.insert(0, "0.1")
        pull.rt7.insert(0, "7")
        pull.tol7.insert(0, "0.1")
        pull.expname.insert(0, "test")
        pull.pickingmethod.set(1)
        with patch("crow.uitabs.Pull.messagebox.showinfo") as test_output:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_output.called)
        pull.clearentriesbutton.invoke()
        self.assertEqual(len(pull.rt1.get()), 0)

        # succcessful operation including retention times
        cg = crow_globals()
        cg.debug = True
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
        ]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "2")
        pull.tol2.insert(0, "0.1")
        pull.rt3.insert(0, "3")
        pull.tol3.insert(0, "0.1")
        pull.rt4.insert(0, "4")
        pull.tol4.insert(0, "0.1")
        pull.rt5.insert(0, "5")
        pull.tol5.insert(0, "0.1")
        pull.rt6.insert(0, "6")
        pull.tol6.insert(0, "0.1")
        pull.rt7.insert(0, "7")
        pull.tol7.insert(0, "0.1")
        pull.expname.insert(0, "test")
        pull.retinclude.set(1)
        pull.pickingmethod.set(1)
        with patch("crow.uitabs.Pull.messagebox.showinfo") as test_output:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_output.called)
        pull.clearentriesbutton.invoke()
        self.assertEqual(len(pull.rt1.get()), 0)

        # succcessful operation with max area, not ret. times
        cg = crow_globals()
        cg.debug = True
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
        ]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "2")
        pull.tol2.insert(0, "0.1")
        pull.rt3.insert(0, "3")
        pull.tol3.insert(0, "0.1")
        pull.rt4.insert(0, "4")
        pull.tol4.insert(0, "0.1")
        pull.rt5.insert(0, "5")
        pull.tol5.insert(0, "0.1")
        pull.rt6.insert(0, "6")
        pull.tol6.insert(0, "0.1")
        pull.rt7.insert(0, "7")
        pull.tol7.insert(0, "0.1")
        pull.expname.insert(0, "test")
        pull.pickingmethod.set(2)
        with patch("crow.uitabs.Pull.messagebox.showinfo") as test_output:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_output.called)
        pull.clearentriesbutton.invoke()
        self.assertEqual(len(pull.rt1.get()), 0)

        # succcessful operation with max area, include ret. times
        cg = crow_globals()
        cg.debug = True
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
        ]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "2")
        pull.tol2.insert(0, "0.1")
        pull.rt3.insert(0, "3")
        pull.tol3.insert(0, "0.1")
        pull.rt4.insert(0, "4")
        pull.tol4.insert(0, "0.1")
        pull.rt5.insert(0, "5")
        pull.tol5.insert(0, "0.1")
        pull.rt6.insert(0, "6")
        pull.tol6.insert(0, "0.1")
        pull.rt7.insert(0, "7")
        pull.tol7.insert(0, "0.1")
        pull.expname.insert(0, "test")
        pull.retinclude.set(1)
        pull.pickingmethod.set(2)
        with patch("crow.uitabs.Pull.messagebox.showinfo") as test_output:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_output.called)
        pull.clearentriesbutton.invoke()
        self.assertEqual(len(pull.rt1.get()), 0)

        # succcessful operation with sll area, not ret. times
        cg = crow_globals()
        cg.debug = True
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
        ]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "2")
        pull.tol2.insert(0, "0.1")
        pull.rt3.insert(0, "3")
        pull.tol3.insert(0, "0.1")
        pull.rt4.insert(0, "4")
        pull.tol4.insert(0, "0.1")
        pull.rt5.insert(0, "5")
        pull.tol5.insert(0, "0.1")
        pull.rt6.insert(0, "6")
        pull.tol6.insert(0, "0.1")
        pull.rt7.insert(0, "7")
        pull.tol7.insert(0, "0.1")
        pull.expname.insert(0, "test")
        pull.pickingmethod.set(3)
        with patch("crow.uitabs.Pull.messagebox.showinfo") as test_output:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_output.called)
        pull.clearentriesbutton.invoke()
        self.assertEqual(len(pull.rt1.get()), 0)

        # succcessful operation with all area, include ret. times
        cg = crow_globals()
        cg.debug = True
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
        ]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "2")
        pull.tol2.insert(0, "0.1")
        pull.rt3.insert(0, "3")
        pull.tol3.insert(0, "0.1")
        pull.rt4.insert(0, "4")
        pull.tol4.insert(0, "0.1")
        pull.rt5.insert(0, "5")
        pull.tol5.insert(0, "0.1")
        pull.rt6.insert(0, "6")
        pull.tol6.insert(0, "0.1")
        pull.rt7.insert(0, "7")
        pull.tol7.insert(0, "0.1")
        pull.expname.insert(0, "test")
        pull.retinclude.set(1)
        pull.pickingmethod.set(3)
        with patch("crow.uitabs.Pull.messagebox.showinfo") as test_output:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_output.called)
        pull.clearentriesbutton.invoke()
        self.assertEqual(len(pull.rt1.get()), 0)

        # succcessful operation with all area, include ret. times
        cg = crow_globals()
        cg.debug = True
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
        ]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "2")
        pull.tol2.insert(0, "0.1")
        pull.rt3.insert(0, "3")
        pull.tol3.insert(0, "0.1")
        pull.rt4.insert(0, "4")
        pull.tol4.insert(0, "0.1")
        pull.rt5.insert(0, "5")
        pull.tol5.insert(0, "0.1")
        pull.rt6.insert(0, "6")
        pull.tol6.insert(0, "0.1")
        pull.rt7.insert(0, "7")
        pull.tol7.insert(0, "0.1")
        pull.expname.insert(0, "test")
        pull.retinclude.set(1)
        pull.pickingmethod.set(4)
        with patch("crow.uitabs.Pull.messagebox.showinfo") as test_output:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_output.called)
        pull.clearentriesbutton.invoke()
        self.assertEqual(len(pull.rt1.get()), 0)

        # wrong input file type
        cg = crow_globals()
        cg.debug = True
        open("blank.csv", "w").close()
        cg.datafiles = [
            "blank.csv",
        ]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        with patch("crow.uitabs.Pull.messagebox.showerror") as test_output:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_output.called)
        os.remove("blank.csv")

        # no data files selected
        cg = crow_globals()
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        with patch("crow.uitabs.Pull.messagebox.showerror") as test_error:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_error.called)

        # intervals overlap
        cg = crow_globals()
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "1.1")
        pull.tol2.insert(0, "0.5")
        with patch("crow.uitabs.Pull.messagebox.showerror") as test_error:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_error.called)

        # intervals out of order
        cg = crow_globals()
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        pull.rt2.insert(0, "0.5")
        pull.tol2.insert(0, "0.1")
        with patch("crow.uitabs.Pull.messagebox.showerror") as test_error:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_error.called)

        # ret. times are not floats
        cg = crow_globals()
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "bad")
        pull.tol1.insert(0, "0.1")
        with patch("crow.uitabs.Pull.mylog") as test_debug:
            with patch("crow.uitabs.Pull.messagebox.showerror") as test_error:
                pull.pulldatabutton.invoke()
                self.assertTrue(test_error.called)
                self.assertTrue(test_debug.called)

        # no retention times/tolerances given
        open("blank.xml", "w").close()
        cg = crow_globals()
        cg.datafiles = [
            "test/data/raw_data_1.xml",
            "test/data/raw_data_2.xml",
            "test/data/raw_data_3.xml",
            "test/data/raw_data_4.xml",
            "test/data/raw_data_5.xml",
            "test/data/raw_data_6.xml",
            "test/data/raw_data_7.xml",
            "test/data/raw_data_8.xml",
            "test/data/raw_data_9.xml",
            "blank.xml",
        ]
        pull = Pull("test pull", cg)
        with patch("crow.uitabs.Pull.messagebox.showerror") as test_error:
            pull.pulldatabutton.invoke()
            self.assertTrue(test_error.called)

        # all files blank
        cg = crow_globals()
        cg.datafiles = ["blank.xml"]
        pull = Pull("test pull", cg)
        pull.rt1.insert(0, "1")
        pull.tol1.insert(0, "0.1")
        with patch("crow.uitabs.Pull.messagebox.showwarning") as test_error:
            with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stderr(devnull):
                    # this test causes an error we would otherwise never see
                    pull.pulldatabutton.invoke()
            self.assertTrue(test_error.called)
        os.remove("blank.xml")
        os.remove(".csv")

    def test_Present(self):
        """

        """
        for layout in range(1, 7):
            for colormap in range(1, 4):
                pass

    def test_cutoff(self):
        """
        Launch the popup for getting the cutoff value in present
        """
        master = tkinter.Tk()
        with patch("crow.utils.popupwindows.cutoff.tk.Toplevel.destroy") as test_close:
            pop = cutoffPopup(master)
            self.assertIsInstance(
                pop,
                cutoffPopup,
            )
            pop.closebutton.invoke()
            self.assertTrue(test_close.called)

    def test_exclude(self):
        """
        Launch the popup to get the wells to exclude
        """
        master = tkinter.Tk()
        with patch("crow.utils.popupwindows.exclude.tk.Toplevel.destroy") as test_close:
            pop = excludePopup(master)
            self.assertIsInstance(
                pop,
                excludePopup,
            )
            pop.closebutton.invoke()
            self.assertTrue(test_close.called)

    def test_numberofcutoffs(self):
        """
        Launch the popup to get the number of cutoffs
        """
        master = tkinter.Tk()
        with patch("crow.utils.popupwindows.numberofcutoffs.tk.Toplevel.destroy") as test_close:
            pop = numberofcutoffsPopup(master)
            self.assertIsInstance(
                pop,
                numberofcutoffsPopup,
            )
            pop.closebutton.invoke()
            self.assertTrue(test_close.called)

    def test_shadebyyield(self):
        """
        Launch the popup to get shade by yield
        """
        master = tkinter.Tk()
        with patch("crow.utils.popupwindows.shadebyyield.tk.Toplevel.destroy") as test_close:
            pop = shadebyyieldPopup(master)
            self.assertIsInstance(
                pop,
                shadebyyieldPopup,
            )
            pop.closebutton.invoke()
            self.assertTrue(test_close.called)


if __name__ == "__main__":
    unittest.main()
