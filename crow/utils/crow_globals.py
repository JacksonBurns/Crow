import yaml
import pkg_resources

"""
Created on Thu Jan 16 19:32:33 2020

@author: jackson
"""


class crow_globals():
    """
    Class which initializes itself using the `config.yaml` file, making
    variables which are used by all tabs of crow accesible in the 'global'
    namespace (but without using global variables).
    """

    def __init__(self, config="config.yaml"):
        """Opens the configuration file and reads the contents into attritbutes.

        Args:
            config (str, optional): Configuration file. Defaults to "config.yaml".
        """
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
