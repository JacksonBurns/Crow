import xml.etree.ElementTree as ET


def ParseXML(filename):
    """
    One line passthrough to xml element tree, returns root of tree

    filename: string which gives either the absolute or relative path
                to an xml file
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    return root
