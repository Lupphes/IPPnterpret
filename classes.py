import xml.etree.ElementTree as ET
from errorCodes import ErrorCodes

class IPPCode20:
    def __init__(self, xml, input):
        structure = Parser(xml.source)
        root = structure.tree.getroot()

        return

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
            command = Instruction(instruction)
            lalal = command.get_class_by_opcode(instruction.attrib['opcode'].lower())
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

class Instruction:
    def __init__(self, tag):
        Parser.validate_argument_keys(tag, "instruction", required=["opcode", "order"], optional=[])
        if tag.attrib["order"] != int:
            print("Order attribute needs to be a whole number")
            exit(ErrorCodes.ERR_XML_SYNTAX.value)


        return

    def get_class_by_opcode(self, opcode: str):
        for item in self.__class__.__dict__.keys():
            if not item.startswith('_'):
                cls = getattr(self, item, None)
                if cls is not None:
                    if opcode in getattr(cls, 'opcode', []):
                            return cls  # Without () so it's just the class
        return None

    # Interactions with frames, function calling #
    class Move:
        opcode = ["move"]
        number_of_args = 2

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class CreateFrame:
        opcode = ["createframe"]
        number_of_args = 0

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class PushFrame:
        opcode = ["pushframe"]
        number_of_args = 0


        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class PopFrame:
        opcode = ["popframe"]
        number_of_args = 0

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Defvar:
        opcode = ["defvar"]
        number_of_args = 1


        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Call:
        opcode = ["call"]
        number_of_args = 1


        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Return:
        opcode = ["return"]
        number_of_args = 0

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    # Interactions with stack  #
    class Pushs:
        opcode = ["pushs"]
        number_of_args = 1


        def __init__(self):
            return   

        @classmethod  
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Pops:
        opcode = ["pops"]
        number_of_args = 1

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    # Arithmetical, relations, bool functions  #
    class Add:
        opcode = ["add"]
        number_of_args = 3
    
        def __init__(self):
            return

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Sub:
        opcode = ["sub"]
        number_of_args = 3
    
        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Mul:
        opcode = ["mul"]
        number_of_args = 3

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class IDiv:
        opcode = ["idiv"]
        number_of_args = 3

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Relation:
        opcode = ["lt", "gt", "eq"]
        number_of_args = 3

        def __init__(self):
            return 

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

        class LT:
            @classmethod
            def create(cls, *args, **kwargs):
                # do something
                return cls(*args, **kwargs)

        class GT:
            @classmethod
            def create(cls, *args, **kwargs):
                # do something
                return cls(*args, **kwargs)

        class EQ:
            @classmethod
            def create(cls, *args, **kwargs):
                # do something
                return cls(*args, **kwargs)

    class Logic:
        opcode = ["and", "or", "not"]
        number_of_args = 3

        def __init__(self):
            return  

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

        class AND:
            def __init__(self):
                return  

            @classmethod
            def create(cls, *args, **kwargs):
                # do something
                return cls(*args, **kwargs)

        class OR:
            def __init__(self):
                return  

            @classmethod
            def create(cls, *args, **kwargs):
                # do something
                return cls(*args, **kwargs)

        class NOT:
            def __init__(self):
                return  
        
            @classmethod
            def create(cls, *args, **kwargs):
                # do something
                return cls(*args, **kwargs)

    class Int2Char:
        opcode = ["int2char"]
        number_of_args = 2

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Stri2Int:
        opcode = ["stri2int"]
        number_of_args = 3

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    # Input/Output  #
    class Read:
        opcode = ["read"]
        number_of_args = 2

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Write:
        opcode = ["write"]
        number_of_args = 1

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    # Interaction with strings  #
    class Concat:
        opcode = ["concat"]
        number_of_args = 3

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Strlen:
        opcode = ["strlen"]
        number_of_args = 2

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Getchar:
        opcode = ["getchar"]
        number_of_args = 3

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Setchar:
        opcode = ["setchar"]
        number_of_args = 3

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    # Interaction with types  #
    class Type:
        opcode = ["type"]
        number_of_args = 2

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    # Flow control  #
    class Label:
        opcode = ["label"]
        number_of_args = 1

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Jump:
        opcode = ["jump"]
        number_of_args = 1

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
         return cls(*args, **kwargs)

    class JumpIfEq:
        opcode = ["jumpifeq"]
        number_of_args = 3

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class JumpIfNeq:
        opcode = ["jumpifneq"]
        number_of_args = 3

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Exit:
        opcode = ["exit"]
        number_of_args = 1

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    # Debug tools
    class DPrint:
        opcode = ["dprint"]
        number_of_args = 1

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)

    class Break:
        opcode = ["break"]
        number_of_args = 0

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)


