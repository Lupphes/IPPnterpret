import xml.etree.ElementTree as ET
from .. import exception
from .. import parser

class Instruction:
    def __init__(self, tag):
        parser.Parser.validate_argument_keys(tag, "instruction", required=["opcode", "order"], optional=[])
        # print(type(tag.attrib["order"]))
        if not tag.attrib["order"].isdigit():
            print("Order attribute needs to be a whole number")
            exit(ErrorCodes.ERR_XML_SYNTAX.value)


        return

    # Interactions with frames, function calling #
class Move(Instruction):
    opcode = "move"
    number_of_args = 2

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class CreateFrame(Instruction):
    opcode = "createframe"
    number_of_args = 0

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class PushFrame(Instruction):
    opcode = "pushframe"
    number_of_args = 0


    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class PopFrame(Instruction):
    opcode = "popframe"
    number_of_args = 0

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Defvar(Instruction):
    opcode = "defvar"
    number_of_args = 1


    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Call(Instruction):
    opcode = "call"
    number_of_args = 1


    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Return(Instruction):
    opcode = "return"
    number_of_args = 0

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Interactions with stack  #
class Pushs(Instruction):
    opcode = "pushs"
    number_of_args = 1


    def __init__(self):
        return   

    @classmethod  
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Pops(Instruction):
    opcode = "pops"
    number_of_args = 1

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Arithmetical, relations, bool functions  #
class Add(Instruction):
    opcode = "add"
    number_of_args = 3

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Sub(Instruction):
    opcode = "sub"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Mul(Instruction):
    opcode = "mul"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class IDiv(Instruction):
    opcode = "idiv"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Relation(Instruction):
    number_of_args = 3

    def __init__(self):
        return 

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class LT(Relation):
    opcode = "lt"
    def __init__(self):
        return 

class GT(Relation):
    opcode = "gt"

    def __init__(self):
        return 

class EQ(Relation):
    opcode = "eq"

    def __init__(self):
        return 

class Logic(Instruction):
    number_of_args = 3

    def __init__(self):
        return  

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class AND(Logic):
    opcode = "and"
    def __init__(self):
        return  

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class OR(Logic):
    opcode = "or"
    def __init__(self):
        return  

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class NOT(Logic):
    opcode = "not"
    def __init__(self):
        return  

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Int2Char(Instruction):
    opcode = "int2char"
    number_of_args = 2

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Stri2Int(Instruction):
    opcode = "stri2int"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Input/Output  #
class Read(Instruction):
    opcode = "read"
    number_of_args = 2

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Write(Instruction):
    opcode = "write"
    number_of_args = 1

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Interaction with strings  #
class Concat(Instruction):
    opcode = "concat"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Strlen(Instruction):
    opcode = "strlen"
    number_of_args = 2

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Getchar(Instruction):
    opcode = "getchar"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Setchar(Instruction):
    opcode = "setchar"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Interaction with types  #
class Type(Instruction):
    opcode = "type"
    number_of_args = 2

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Flow control  #
class Label(Instruction):
    opcode = "label"
    number_of_args = 1

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Jump(Instruction):
    opcode = "jump"
    number_of_args = 1

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class JumpIfEq(Instruction):
    opcode = "jumpifeq"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class JumpIfNeq(Instruction):
    opcode = "jumpifneq"
    number_of_args = 3

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Exit(Instruction):
    opcode = "exit"
    number_of_args = 1

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Debug tools
class DPrint(Instruction):
    opcode = "dprint"
    number_of_args = 1

    def __init__(self):
        return        

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

class Break:
        opcode = "break"
        number_of_args = 0

        def __init__(self):
            return        

        @classmethod
        def create(cls, *args, **kwargs):
            # do something
            return cls(*args, **kwargs)
