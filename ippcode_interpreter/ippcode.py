import xml.etree.ElementTree as ET
from .parser import Parser


class IPPCode21:
    """ Main function of the interpret, creates the code structure and evaluate it """

    def __init__(self, source, input):
        parsed_code = Parser(source, input)
        # print(parsed_code.instruction_string)
        # print(parsed_code.resourses)
        exec(parsed_code.instruction_string, parsed_code.resourses)
        return
