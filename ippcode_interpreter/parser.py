import xml.etree.ElementTree as ET
from . import instructions

class Parser:
    def __init__(self, args):

        try:
            tree = ET.parse(args)
        except ET.ParseError:
            print("XML Parse error")
            exit(ErrorCodes.ERR_XML_SYNTAX.value)
        except: 
            print("General XML error")
            exit(ErrorCodes.ERR_INTERNAL.value)
        
        # Program tag validation
        root = tree.getroot()
        self.validate_header(root)

        for instruction in root:
            instructions.Instruction(instruction)
            lalal = instructions.get_class_by_opcode(instruction.attrib['opcode'].lower())
            # if 
            print(lalal)
            print("lalala")
            # print(instruction.tag + " || " + str(instruction.attrib))


        # sorted_tree = sorted(root, key=lambda child: child.attrib["order"])
        
        # for instruction in sorted_tree:
        #     print(instruction.tag + " || " + instruction.attrib["order"])

        self.tree = tree
        return 



    @staticmethod
    def validate_header(tag):
        Parser.validate_argument_keys(tag, "program", required=["language"], optional=["name", "description"])
        Parser.validate_argument_values(tag.attrib, possibleValues={"language": ["ippcode21"]})
        return

    @staticmethod
    def validate_argument_keys(tag, name, required, optional=[]):
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
    def validate_argument_values(attributes, possibleValues):
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
