""" Test the methods of Crow."""
import os
import sys
import unittest
from unittest.mock import patch

from crow.Crow import main
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

        """
        pass

    def test_PrePull(self):
        """

        """
        pass

    def test_Pull(self):
        """

        """
        pass

    def test_Present(self):
        """

        """
        pass

    def test_cutoff(self):
        """

        """
        pass

    def test_exclude(self):
        """

        """
        pass

    def test_numberofcutoffs(self):
        """

        """
        pass

    def test_shadebyyield(self):
        """

        """
        pass


if __name__ == "__main__":
    unittest.main()

"""
Test all internal methods for the Crow application which do not rely on user input.

Other functions which do require user input can be tested by running Crow.py and entering
the provided sample raw data and sample input data in the test directory, ex.:

    python Crow.py

    In the User Interface, navigate to the PrePull or Pull tab.
    Press the "Select Raw Data" button and, when prompted, select
        the .xml files provided in /test/Sample GC Data
    Click Pre-Pull to generate of histogram of all eluates and
        setup and run a Pull to retrieve some desired peak(s).
    Navigate to the present tab.
    Press the "Select Excel Data" button and navigate to the
        sample input data provided in /test
    Experiment with various layouts, filters, and with exporting
        generated plots.
"""


# """
# Test PrePull_GC.py
# """
# PrePull_test = PrePull_GC.PrePull("Pre-Pull")
# # ensure that tab is properly instantiated
# assert isinstance(PrePull_test, PrePull_GC.PrePull)
# # it is technically possible to generate "virtual events" like this:
# # PrePull_test.event_generate("<<prepullcallback>>")
# # such as button clicks, it is difficult to interact with the results.
# # Manual testing with example data will still show proper functioning of
# # methods.
# """
# Test Pull_GC.py
# """
# Pull_test = Pull_GC.Pull("Pull")
# # ensure that tab is properly instantiated
# assert isinstance(Pull_test, Pull_GC.Pull)
# """
# Test Present_GC.py
# """
# Present_test = Present_GC.Present("Present")
# # ensure that tab is properly instantiated
# assert isinstance(Present_test, Present_GC.Present)
