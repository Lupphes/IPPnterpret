import xml.etree.ElementTree as ET
from . import instructions as inst
from .exception import ErrorCodes
from typing import List, Dict
import logging


class Parser:
    """ Parses the whole source XML tree and provides the input which is needed for the interpret to run """

    def __init__(self, source, input):

        try:
            parsed_tree = ET.parse(source)
        except ET.ParseError:
            logging.error("XML Parse error")
            exit(ErrorCodes.ERR_XML_SYNTAX.value)
        except:
            logging.error("General XML error")
            exit(ErrorCodes.ERR_INTERNAL.value)

        # Program tag validation
        program_tag = parsed_tree.getroot()
        self.validate_header(program_tag)

        self.code_string = ""

        for instruction_tag in program_tag:
            inst.Instruction(instruction_tag)
            created_instruction = inst.get_class_by_opcode(
                opcode=instruction_tag.attrib['opcode'].lower()
            )

            if (created_instruction == None):  # If instruction doesn't exist
                logging.error("Specified instruction doesn't exist")
                exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)

            created_instruction.validate_arguments(
                self=created_instruction,
                tag=instruction_tag
            )

            print(created_instruction)
            print(created_instruction.args)

        # sorted_tree = sorted(root, key=lambda child: child.attrib["order"])

        # for instruction in sorted_tree:
        #     print(instruction.tag + " || " + instruction.attrib["order"])

        self.tree = parsed_tree
        return

    @staticmethod
    def validate_header(program_tag: ET.Element) -> None:
        """ Validates the program tag, root tag of the program """
        Parser.validate_tag_keys(program_tag, "program", required=[
                                 "language"], optional=["name", "description"])
        Parser.validate_tag_values(program_tag.attrib, possibleValues={
                                   "language": ["ippcode20"]})
        return

    @staticmethod
    def validate_tag_keys(tag: ET.Element, name: str, required: List, optional: List = []) -> None:
        """ Provides validation of tag keys """
        if tag.tag != name:  # Validates the name of the tag
            logging.error(f"'{tag.tag}' is not valid XML tag in this context")
            exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)
        for tag_desc in required:
            if tag_desc in tag.attrib.keys():
                continue
            elif tag_desc not in optional:  # If not in the optional, the tag is incorrect
                logging.error("Incorrect argument in XML")
                exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)
        return

    @staticmethod
    def validate_tag_values(attributes: Dict, possibleValues: Dict) -> None:
        """ Provides validation of tag values """
        for artrib in attributes:
            for possible_valid in possibleValues:
                if artrib == possible_valid:
                    successful = False
                    for item in possibleValues[possible_valid]:
                        if attributes[possible_valid].lower() == item.lower():
                            successful = True
                            break
                    if not successful:
                        logging.error(
                            "Argument doesn't have correct syntax. Probably header")
                        exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)
        return
