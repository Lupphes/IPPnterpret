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

        label_string = "["
        instruction_code = ""
        resourses = {

        }

        sorted_tree = sorted(program_tag, key=self.validate_order)

        for key, instruction_tag in enumerate(sorted_tree):
            if (key > 0):
                if sorted_tree[key].attrib["order"] != sorted_tree[key-1].attrib["order"]:
                    previous_number = instruction.order
                else:
                    logging.error("The instructions order can't be duplicated")
                    exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)

            instruction_class = inst.get_class_by_opcode(
                opcode=instruction_tag.attrib['opcode'].lower()
            )

            if (instruction_class == None):  # If instruction doesn't exist
                logging.error("Specified instruction doesn't exist")
                exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)

            instruction_class.validate_arguments(
                self=instruction_class,
                tag=instruction_tag
            )
            instruction = instruction_class(instruction_tag)
            if instruction.opcode == "label":
                label_string += self.get_label_from_instruction(instruction)+", "
                
            # print(instruction)
            # print(instruction.args)
            # print(instruction.order)
            resourses.update({str(instruction.__class__.__name__): instruction})
            instruction_code += instruction.__class__.__name__ + ".run()\n"

        # self.tree = parsed_tree
        label_string = "]" if label_string == "[" else label_string[:-2] + "]"
        self.label_string = label_string
        self.instruction_string = instruction_code
        self.resourses = resourses
        # print(label_string)
        # print(instruction_code)
        return

    def get_label_from_instruction(self, label_class) -> dict:
        temp = {
            "order": label_class.order,
            "value": label_class.args[0]["value"]
        }
        return str(temp)

    def validate_order(self, tag: ET.Element) -> int:
        """ Checks if attribute order is valid """
        Parser.validate_tag_keys(
            tag=tag,
            name="instruction",
            required=["opcode", "order"],
            optional=[]
        )
        if not (tag.attrib["order"].isdigit() and int(tag.attrib["order"]) > 0):
            logging.error(
                "Order attribute needs to be a whole number bigger that 0")
            exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)

        return int(tag.attrib["order"])

    @staticmethod
    def validate_header(program_tag: ET.Element) -> None:
        """ Validates the program tag, root tag of the program """
        Parser.validate_tag_keys(program_tag, "program", required=[
                                 "language"], optional=["name", "description"])
        Parser.validate_tag_values(program_tag.attrib, possibleValues={
                                   "language": ["ippcode20"]})
        return

    @staticmethod
    def validate_tag_keys(tag: ET.Element, name: str, required: list, optional: list = []) -> None:
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
    def validate_tag_values(attributes: dict, possibleValues: dict) -> None:
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
