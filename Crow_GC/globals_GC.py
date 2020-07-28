# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 19:32:33 2020

@author: jackson
"""


def init():
    """
    variables which are used by all tabs in the GC window, such as the path to
    the server of raw data.
    """
    global datafiles
    datafiles = []
    global rawdatapath
    rawdatapath = r"W:\data\XML_EXPORT\\"
    global exportdatapath
    exportdatapath = r"C:\Users\jwb1j\OneDrive\Desktop\hte output data\\"
