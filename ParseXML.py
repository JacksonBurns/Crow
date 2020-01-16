#!/usr/bin/python3.6
import xml.etree.ElementTree as ET
def ParseXML(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root