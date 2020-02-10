# Crow
Crow Really Outta Work

## What is Crow?
Crow is a software package for retrieving, diagnosing, and presenting High Throughput Experimentation data from various instruments.

Crow has three tabs: __Pre-Pull__, __Pull__, and __Present__. __Pre-Pull__ identifies all peaks (and their areas) present in a given data set and generates a histogram of elution times. This is intended to help the user decide on a retention time (and small tolerance window) for each eluate to be pulled from the instrument data. With the help of __Pre-Pull__, __Pull__ enables users to apidly retrieve the peak areas for large datasets and export them to an Excel file (.csv) for easy manipulation. __Present__ takes Excel files including _only_ the data to be placed in the pie charts, which can then be filtered in a variety of ways to better represent multivariate data.

Designed by Jackson Burns at the University of Delaware Donald Watson Lab in 2019, coded in Python in 2020.

## How to use Crow
Please see the video below for instructions:
<video src="Crow-SOP.mp4" poster="Crow_logo.png" width="320" height="200" controls preload></video>

## Setup
Data is retrieved by parsing XML files output by the software on the High Throughput Experimentation instrument. For example, our setup uses an Agilent GC and their software to run experiments and calculate eluate peak areas.

A conda environment file (.yml) lists the required packages and versions needed to run Crow.

To configure Crow to work for your setup, there are a few small changes to make:
* change the filepath in PrePull "Search Server by Name" callback to the location of your network drive where xml data are stored
* change the indexing in Pull to match the location of the peak data in your particular instrument's output files
  
## Support
If you need help with setting up Crow, finding out how to retrieve data from your HTE instrument, or you find this program at all helpful, send me a message here: jburnsky@udel.edu with the subject line "Crow"
