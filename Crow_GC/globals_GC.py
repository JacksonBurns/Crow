import yaml

"""
Created on Thu Jan 16 19:32:33 2020

@author: jackson
"""


def init():
    """
    variables which are used by all tabs in the GC window, such as the path to
    the server of raw data.
    """
    # open the config file, do not need to use absolute import because this file
    # will always be run by Crow.py, which is in the same directory
    with open("config.yaml", "r") as file:
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
