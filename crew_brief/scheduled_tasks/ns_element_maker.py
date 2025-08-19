import xml.etree.ElementTree as ET

class NSElementMaker:
    """
    Automatically add namespace to elements.
    """

    def __init__(self, namespace):
        self.namespace = namespace

    def __call__(self, tag, text=None, attrib=None):
        el = ET.Element(f'{{{self.namespace}}}{tag}', attrib or {})
        if text:
            el.text = text
        return el
