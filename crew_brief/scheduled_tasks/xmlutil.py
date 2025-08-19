import xml.etree.ElementTree as ET

from xml.dom import minidom

def pretty_xml(element_tree):
    rough_string = ET.tostring(element_tree.getroot(), 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent='    ')
