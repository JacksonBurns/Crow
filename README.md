# Crow - Accelerating High Throughput Experimentation
![Crow Logo](/Crow/other/Crow_logo.png)

![GitHub Repo stars](https://img.shields.io/github/stars/JacksonBurns/Crow?style=social)
![PyPI - Downloads](https://img.shields.io/pypi/dm/CrowHTE)
![PyPI](https://img.shields.io/pypi/v/CrowHTE)
![PyPI - License](https://img.shields.io/pypi/l/CrowHTE)

Crow is a software package for retrieving, diagnosing, and presenting High Throughput Experimentation data from various instruments. Designed by Jackson Burns at the University of Delaware Donald Watson Lab in 2019, coded in Python in 2020 and still under active development.

## Installation and Setup
Crow can be installed from the python package index (PyPi) with the following command:

`pip install CrowHTE`

Crow can then be started by typing `crow` in the command line.

A step-by-step setup tutorial, including how to set up a python environment and access this repository, is [available here](https://github.com/JacksonBurns/Crow/blob/main/Crow/other/setup_step-by-step.md).

To configure Crow to work for your instruments, modify __config.yaml__ to work for your local installation. Data is retrieved by parsing XML files output by the software on the High Throughput Experimentation instrument. For example, our setup uses an Agilent GC and their software to run experiments and calculate eluate peak areas. Again, for an in-depth setup tutorial, see [here](https://github.com/JacksonBurns/Crow/blob/main/Crow/other/setup_step-by-step.md).

## Using Crow
Crow has three tabs: __Pre-Pull__, __Pull__, and __Present__. __Pre-Pull__ identifies all peaks (and their areas) present in a given data set and generates a histogram of elution times. This is intended to help the user decide on a retention time (and small tolerance window) for each eluate to be pulled from the instrument data. With the help of __Pre-Pull__, __Pull__ enables users to rapidly retrieve the peak areas for large datasets and export them to an Excel file (.csv) for easy manipulation. __Present__ takes Excel files including _only_ the data to be placed in the pie charts, which can then be filtered in a variety of ways to better represent multivariate data.

The above information is also explained in the video tutorial below:
[Crow SOP](/Crow/other/Crow-SOP.mp4)

## Support
If you need help with setting up Crow, finding out how to retrieve data from your HTE instrument, or you find this program at all helpful, send me a message.

To contribute to project, report or a bug, or request a new feature, open a pull request using one of the provided templates.
