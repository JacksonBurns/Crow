---
title: 'Crow: A Python GUI for Optimizing High Throughput Experimentation'
tags:
  - Python
  - tkinter
  - High Throughput Experimentation
  - Gas Chromatography
  - Cheminformatics
authors:
  - name: Jackson W. Burns
    affiliation: 1 # (Multiple affiliations must be quoted)
  - name: Katerina M. Korch
    affiliation: 1
  - name: Donald A. Watson
    affiliation: "1, 2"
affiliations:
  - name: University of Delaware, Donald A. Watson Lab
    index: 1
  - name: University of Delaware  High Throughput Experimentation Center
    index: 2
date: 29 July 2020
bibliography: paper.bib

---

# Statement of Need

The advent of High Throughput Experimentation (HTE) techniques has enabled
scientists of all disciplines to drastically increase the pace of discovery and
graduate from resource-intense, Edisonian science. In particular, the pairing of HTE
with gas chromatography has been of special interest [@Shevlin:2018], as it enables
the simultaneous execution of dozens or even hundreds of experiments. The implementation 
of such groundbreaking technologies in the academic space, however, has been hampered
by the lack of automation in the retrieval, processing, and interpretation of data. 
Commercial solutions are prohibitively expensive, closed-source, and often require
additional of HTE equipment, meaning existing technologies cannot be carried forward.

# Summary

'Crow' seeks to remedy this problem by making HTE practical in an academic setting.
The package is platform-agnostic and highly customizable, allowing users to modify
key application parameters through a simple *config.yaml* file. Data is retrieved
via the *.xml* format, in which nearly all lab equipment can export data. The core functionality
of 'Crow' is accessed via a simple multi-tab graphical user interface, enabling walk-up
use for non-coding users post-configuration. Commonly accessed internal functions are separate
so they may be compiled into bytecode via CPython to decrease execution time after initial
compilation.

In its current GC implementation, 'Crow' has three tabs which access its main functions: 
**Pre-Pull**, **Pull**, and **Present**. **Pre-Pull** identifies all peaks present in a 
user-selected data set and generates a histogram of elution times. This is intended to help
the user decide on a retention time and small tolerance window for each eluate when retrieved
from the instrument data. **Pull** then asks users to specify a set of retention times
and tolerances for expected eluates, before rapidly parsing all the data and retrieving
only some given value for peaks which the user requested, such as area. The resulting data
is output to the universal *.csv* for easy manipulation in the users software of choice.
**Present** ingests *.csv* files and generates graphics resembling a multi-well plate of
pie charts. Data can then be manipulated in a variety of ways to represent multivariate data
such as in \autoref{fig:Example **Present** output}. All plots and graphics are created with
'matplotlib' [@Caswell:2020] which enables exporting in multiple common image formats.

![Example 96 well plate used for ligand screening in a Heck Reaction, here using the included 
deuteranopia-friendly color palette.\label{fig:Example **Present** output}](example_present_output.png)

'Crow' has been implemented in the following publication and is used in the University of Delaware
High Throughput Experimentation Center.

# Acknowledgements

We acknowledge funding from the University of Delaware Undergraduate Research Program Stakem Grant.

# References
