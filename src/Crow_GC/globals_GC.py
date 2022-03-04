import yaml
import traceback
from datetime import datetime
import pkg_resources

"""
Created on Thu Jan 16 19:32:33 2020

@author: jackson
"""


def init():
    """
    variables which are used by all tabs in the GC window, such as the path to
    the server of raw data.
    """
    # open the config file
    resource_path = pkg_resources.resource_filename(__name__, "config.yaml")
    with open(resource_path, "r") as file:
        cfg = yaml.safe_load(file)
    cfg = cfg["GC_config"]
    global datafiles
    datafiles = []
    global rawdatapath
    rawdatapath = cfg["server_data_location"]
    global debug
    debug = cfg["debug"]
    global exportdatapath
    exportdatapath = cfg["export_data_path"]
    global peaktarg
    peaktarg = cfg["xml_peaks_target"]
    global rettarg
    rettarg = cfg["xml_retention_time_target"]
    global areatarg
    areatarg = cfg["xml_area_target"]
    global roundres
    roundres = cfg["pre_pull_rounding_resolution"]
    global welltarg
    welltarg = cfg["xml_wellnum_target"]


def mylog(e):
    """
    General purpose function for writing errors to an external .txt file

    e: exception raised by one of the three tabs of Crow GC
    """
    debugfile = open("debug.txt", "a")
    debugfile.write("\n")
    debugfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " - " + str(e))
    debugfile.write("\n")
    debugfile.write(traceback.format_exc())
    debugfile.write("\n")
    debugfile.close()
