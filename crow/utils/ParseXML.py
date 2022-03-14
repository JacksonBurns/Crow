import xml.etree.ElementTree as ET


def ParseXML(filename):
    """One line passthrough to xml element tree.

    Args:
        filename (string): the absolute or relative path to an xml file

    Returns:
        etree: root of tree
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    return root
