# Step-by-Step Crow Setup Tutorial

If you have already completed or are familiar with a given section, skip ahead to the next applicable section.


## Setting up lab equipment to export *xml* files
This is going to vary a lot depending on your indivudal equipment, but for our Agilent 6890 it went like this:
1. Modify the *settings.ini* file for the instrumet to:
	- enable *xml* exporting
	- specify an export path, in our case to a metwork drive
2. Restart the associated sfotware to apply the settings

Finding out exactly how to do this (in terms of settigns to modify/keywords to use) would probably
be found in the manual for your instrument. It took us a bit of searching, but once you find it
the process is simple.


## Setting up a Python Environment
Python allows you to create *virtual environments* that contain only the packages (with their appropriate versions) that a program needs. We reccomend using one like this:
1. Download the package manager of your choice - these instructions use conda and [Anaconda Navigator](https://docs.anaconda.com/anaconda/navigator/), the GUI passthrough to conda.
2. In anaconda navigator, create a new environment by selecting "Create".
3. Once the environment builds, launch a terminal window through the "Home" tab.


## Downloading and Configuring Crow
There are a few options for downloading Crow (figshare, GitHub, PyPi) but it is best to do this:
`pip install CrowHTE`
If any import statements fail, use **pip** or **conda** to install missing packages. (Please also consider filing a [bug report](https://github.com/JacksonBurns/Crow/issues))
If you would instead like to download the code directly from a website, do the following:
1. Follow [this](https://github.com/JacksonBurns/Crow/releases) link to the *Crow* repository on GitHub.
2. Download the Zip file containing the source code for Crow.
3. Un-Zip the code into a new folder.

Once Crow has been installed, edit the *config.yaml* file and adjust the below fields accordingly:
	- server_data_location: This should point to a mapped drive on the system where Crow is running. Crow can automatically search this location for raw data. ex. W:\data\XML_EXPORT\
    - debug: Writes a *debug.txt* file containing exceptions and timestamps.
    - export_data_path:This should point to the location where you want pulled data to be saved. ex. /usr/me/hte_data/
    - pre_pull_rounding_resolution: This value determines how the retention are binned in the pre-pull diagnostic histogram.
    - xml_peaks_target: These two values should indicate the location of the peak data in the *xml* file.
    - xml_retention_time_target: Index of the retention time value for each peak.
    - xml_area_target: Index of the area value for each peak (can be set to any desired value, such as index of width)
    - xml_wellnum_target: Index of the well number which each peak should contain, which references the experimental well that the data came from.
If you used pip to install Crow, the config file will probably be found in your-user-folder/.conda/envs/your-environment-name/Lib/site-packages/Crow/Crow_GC. If you downloaded the code from online, the configuration file will be in Crow/Crow_GC.


## Using Crow
Crow can be started from the command line by typing `crow`. You can also start Crow from inside a python script like this:
`
from Crow import Crow
Crow.main()
`
For a video tutorial on how to use Crow, [Crow SOP](Crow-SOP.mp4).

### Selecting Data
1. Enter a *glob*-compatible string which Crow will use to search the 'server' location or manually select input data.
2. Ensure that the correct files and correct numebr of files were selected.
### Pre-Pull
1. Once Data files are selected, press the button on the **Pre-Pull** tab to generate a historam of elution times.
2. Using the zoom and pan functionality, find groups of peaks which represent desired eluates such as product, starting material, standard, etc.
3. Note the retention time and an approximate 'window' where these peaks are grouped.
### Pull
1. Navigate to the pull tab, still with the same data files selected.
2. Enter the decided upon retention times and tolerance windows.
3. Provide a name for the output file.
4. Select the peak peaking method.
5. Select if retntion times should be included.
6. Press the **Pull Data** button.
### Present
1. After manipulating the data to reflect yield, selectivity, etc. style the data in the form of the given sample data.
2. Return to Crow and select the data via the button.
3. Select the size and orientation of the experiment.
4. Select appropriate filters and settings.
5. Generate the graph, and experiment with other settings.
6. Export the graphic (if needed)
