import xml.etree.ElementTree as ET
from . import instructions as inst
from .exception import InvalidXMLSyntax, XMLParsingError, IPPCodeSyntaxError


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

        label_string = "["
        mangled_instructions = []

        for key, instruction_tag in enumerate(sorted_tree):
            if key > 0:
                if sorted_tree[key].attrib["order"] != sorted_tree[key-1].attrib["order"]:
                    previous_number = instruction.order
                else:
                    raise IPPCodeSyntaxError(
                        "The order must be unique for each instruction")

            instruction_class = inst.get_class_by_opcode(
                opcode=instruction_tag.attrib['opcode'].lower()
            )

            if instruction_class is None:  # If instruction doesn't exist
                raise IPPCodeSyntaxError("Specified instruction doesn't exist")

            instruction_class.validate_arguments(
                self=instruction_class,
                tag=instruction_tag
            )

            instruction = instruction_class(instruction_tag)
            if instruction.opcode == "label":
                label_string += self.get_label_from_instruction(
                    instruction) + ", "

            mangled_instructions.append({
                instruction.create_mangled_name(instruction.order): instruction
            })

        label_string = "]" if label_string == "[" else label_string[:-2] + "]"
        self.label_string = label_string
        self.mangled_instructions = mangled_instructions

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
            possibleValues={"language": ["ippcode20"]}
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
