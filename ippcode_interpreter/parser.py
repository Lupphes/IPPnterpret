import xml.etree.ElementTree as ET
from . import instructions as inst
from .exception import InvalidXMLSyntax, XMLParsingError, IPPCodeSyntaxError

import sys


class Parser:
    """ Parses the whole source XML tree and provides the input which is needed for the interpret to run """

    def __init__(self, source, input):

        try:
            parsed_tree = ET.parse(source)
        except ET.ParseError:
            raise InvalidXMLSyntax()
        except:
            raise XMLParsingError()

        # Program tag validation
        program_tag = parsed_tree.getroot()
        self.validate_header(program_tag)

        sorted_tree = sorted(program_tag, key=self.validate_order)

        self.mangled_instructions = {
            "instructions": [],
            "labels": {}
        }

        self.program_length = len(sorted_tree)

        previous_label = None

        for index, instruction_tag in enumerate(sorted_tree):
            if index > 0:
                if sorted_tree[index].attrib["order"] != sorted_tree[index-1].attrib["order"]:
                    previous_number = instruction.order
                else:
                    raise IPPCodeSyntaxError(
                        "The order must be unique for each instruction"
                    )

            instruction_class = inst.get_class_by_opcode(
                opcode=instruction_tag.attrib['opcode'].lower()
            )
            if instruction_class is None:  # If instruction doesn't exist
                raise IPPCodeSyntaxError("Specified instruction doesn't exist")

            instruction = instruction_class(instruction_tag)
            if instruction.opcode == "label":
                new_label = instruction.args[0]["value"]

                if new_label in self.mangled_instructions["labels"]:
                    sys.exit(52)
                else:
                    instruction.define(start=index, end=self.program_length - 1)
                    if previous_label is not None:
                        start = self.mangled_instructions["labels"][previous_label].start
                        end = index - 1
                        self.mangled_instructions["labels"][previous_label].define(
                            start=start, 
                            end=end
                        )

                    self.mangled_instructions["labels"][new_label] = instruction
                    previous_label = new_label
                    
                    self.mangled_instructions["instructions"].append(instruction)
            else:
                self.mangled_instructions["instructions"].append(
                    instruction)

    def get_label_from_instruction(self, label_class) -> dict:
        return {
            "order": label_class.order,
            "value": label_class.args[0]["value"]
        }

    def validate_order(self, tag: ET.Element) -> int:
        """ Checks if attribute order is valid """
        Parser.validate_tag_keys(
            tag=tag,
            name="instruction",
            required=["opcode", "order"],
            optional=[]
        )
        if not (tag.attrib["order"].isdigit() and int(tag.attrib["order"]) > 0):
            raise IPPCodeSyntaxError(
                "Order attribute needs to be a whole number bigger that 0")

        return int(tag.attrib["order"])

    @staticmethod
    def validate_header(program_tag: ET.Element) -> None:
        """ Validates the program tag, root tag of the program """
        Parser.validate_tag_keys(
            tag=program_tag,
            name="program",
            required=["language"],
            optional=["name", "description"]
        )
        Parser.validate_tag_values(
            attributes=program_tag.attrib,
            possibleValues={"language": ["ippcode21"]}
        )
        return

    @staticmethod
    def validate_tag_keys(tag: ET.Element, name: str, required: list, optional: list = []) -> None:
        """ Provides validation of tag keys """
        if tag.tag != name:  # Validates the name of the tag
            raise IPPCodeSyntaxError(
                f"'{tag.tag}' is not valid XML tag in this context")
        for tag_desc in required:
            if tag_desc in tag.attrib.keys():
                continue
            elif tag_desc not in optional:  # If not in the optional, the tag is incorrect
                raise IPPCodeSyntaxError("Specified argument is not valid")
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
                        raise IPPCodeSyntaxError(
                            "Specified argument is not valid; Probably header")
        return
