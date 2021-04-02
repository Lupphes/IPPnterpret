import xml.etree.ElementTree as ET
from . import instructions as inst

class Parser:
    """ Parses the whole source XML tree and provides the input which is needed fro the interpret to run """
    def __init__(self, source, input):

        try:
            parsed_tree = ET.parse(source)
        except ET.ParseError:
            print("XML Parse error")
            exit(ErrorCodes.ERR_XML_SYNTAX.value)
        except: 
            print("General XML error")
            exit(ErrorCodes.ERR_INTERNAL.value)
        
        # Program tag validation
        root_tag = parsed_tree.getroot()
        self.validate_header(root_tag)
        self.code_string = ""

        for opcode_tag in root_tag:
            inst.Instruction(opcode_tag)
            created_opcode = inst.get_class_by_opcode(opcode_tag.attrib['opcode'].lower())
            created_opcode.validate_arguments(created_opcode, opcode_tag)

            
            print(created_opcode)


        # sorted_tree = sorted(root, key=lambda child: child.attrib["order"])
        
        # for instruction in sorted_tree:
        #     print(instruction.tag + " || " + instruction.attrib["order"])

        self.tree = parsed_tree
        return 

    @staticmethod
    def validate_header(tag):
        """ Validates the header of the program """
        Parser.validate_tag_keys(tag, "program", required=["language"], optional=["name", "description"])
        Parser.validate_tag_values(tag.attrib, possibleValues={"language": ["ippcode21"]})
        return

    @staticmethod
    def validate_tag_keys(tag, name, required, optional=[]):
        """ Provides validation of tag keys """
        if tag.tag != name:
            print(f"'{tag.tag}' is not valid XML tag in this context")
            exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)
        correct = False
        for elem in tag.attrib.keys():
            if elem in required:
                correct = True
            elif elem not in optional:
                print("Incorrect argument in XML")
                exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)
            
        if correct is False:
            print("Required argument in XML not found")
            exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)
        return

    @staticmethod
    def validate_tag_values(attributes, possibleValues):
        """ Provides validation of tag values """
        for artrib in attributes:
            for key in possibleValues:
                if artrib == key:
                    successful = False
                    for item in possibleValues[key]:
                        if attributes[key].lower() == item.lower():
                            successful = True
                            break
                    if not successful:
                        print("Argument doesn't have correct syntax")
                        exit(ErrorCodes.ERR_XML_UNEXPECTED_STRUCT.value)
        return
