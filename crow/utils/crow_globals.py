import yaml
import pkg_resources

"""
Created on Thu Jan 16 19:32:33 2020

@author: jackson
"""


class crow_globals():
    """
    variables which are used by all tabs in the window, such as the path to
    the server of raw data.
    """

    def __init__(self, config="config.yaml"):
        # open the config file
        if config == "config.yaml":
            resource_path = pkg_resources.resource_filename(
                __name__, config)
        else:
            resource_path = config
        with open(resource_path, "r") as file:
            cfg = yaml.safe_load(file)
        cfg = cfg["config"]
        self.datafiles = []
        self.rawdatapath = cfg["server_data_location"]
        self.debug = cfg["debug"]
        self.exportdatapath = cfg["export_data_path"]
        self.peaktarg = cfg["xml_peaks_target"]
        self.rettarg = cfg["xml_retention_time_target"]
        self.areatarg = cfg["xml_area_target"]
        self.roundres = cfg["pre_pull_rounding_resolution"]
        self.welltarg = cfg["xml_wellnum_target"]
