import xml.etree.ElementTree as ET
from .parser import Parser


class IPPCode21:
    """ Main function of the interpret, creates the code structure and evaluate it """

    def __init__(self, source, input):
        structure = Parser(source, input)
        return
