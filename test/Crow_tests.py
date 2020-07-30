import sys
import os
sys.path.insert(0, '..')
initdir = os.getcwd()
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

"""
Test globals_GC.py
"""
# test initialization of global variables and debug function
os.chdir("Crow_GC")
from Crow_GC import globals_GC
# write a temporary config file for testing purposes
with open("config.yaml", "w") as file:
    file.writelines([
        "GC_config:\n",
        "    server_data_location: Z:\\test\\server_data\\\n",
        "    debug: True\n",
        "    export_data_path: Z:\\test\\export_data\\\n",
        "    pre_pull_rounding_resolution: 0.0025\n",
        "    xml_peaks_target: [8, 6]\n",
        "    xml_retention_time_target: 9\n",
        "    xml_area_target: 15\n",
        "    xml_wellnum_target: [1, 12]\n"])
# run global setup
globals_GC.init()
# ensure that all the given variables were assigned correctly
assert globals_GC.datafiles == []
assert globals_GC.debug
assert globals_GC.rawdatapath == "Z:\\test\\server_data\\"
assert globals_GC.exportdatapath == "Z:\\test\\export_data\\"
assert globals_GC.peaktarg == [8, 6]
assert globals_GC.rettarg == 9
assert globals_GC.areatarg == 15
assert globals_GC.roundres == 0.0025
assert globals_GC.welltarg == [1, 12]
# test eexception logger
try:
    # intentionally cause an exception
    3 / 0
except Exception as e:
    globals_GC.mylog(e)
assert os.path.isfile("debug.txt")
# remove file to prevent cluttering
os.remove("debug.txt")

"""
Test PrePull_GC.py
"""
from Crow_GC import PrePull_GC
PrePull_test = PrePull_GC.PrePull("Pre-Pull")
# ensure that tab is properly instantiated
assert isinstance(PrePull_test, PrePull_GC.PrePull)
# it is technically possible to generate "virtual events" like this:
# PrePull_test.event_generate("<<prepullcallback>>")
# such as button clicks, it is difficult to interact with the results.
# Manual testing with example data will still show proper functioning of
# methods.
"""
Test Pull_GC.py
"""
from Crow_GC import Pull_GC
Pull_test = Pull_GC.Pull("Pull")
# ensure that tab is properly instantiated
assert isinstance(Pull_test, Pull_GC.Pull)
"""
Test Present_GC.py
"""
from Crow_GC import Present_GC
Present_test = Present_GC.Present("Present")
# ensure that tab is properly instantiated
assert isinstance(Present_test, Present_GC.Present)

# remove temporary file
os.remove("config.yaml")

"""
Test helper functions which do not rely on GUI-based user input.

Those helper functions which do require input are tested by executing
the tests described at the top of this document.
"""
# write a temporary xml file to test ParseXML.py
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
import Crow_GC
root_test = Crow_GC.Crow_GC.ParseXML.ParseXML("temp.xml")
# check various parts of the returned root to ensure that it is read correctly
assert root_test[0].text == "1"
assert root_test[2].text == "Agilent 6890 GC"
assert root_test[5].text == "6890"
# remove temporary file
os.remove("temp.xml")
