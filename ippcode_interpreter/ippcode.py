import xml.etree.ElementTree as ET
from . import parser

class IPPCode20:
    def __init__(self, xml, input):
        structure = parser.Parser(xml.source)
        root = structure.tree.getroot()

        return