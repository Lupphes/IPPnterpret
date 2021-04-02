import xml.etree.ElementTree as ET
from ..exception import ErrorCodes
from ..parser import Parser


class Instruction:
    def __init__(self, tag):
        self.tag = tag
        Parser.validate_tag_keys(tag, "instruction", required=[
                                             "opcode", "order"], optional=[])
        if not (tag.attrib["order"].isdigit() and int(tag.attrib["order"]) > 0):
            print("Order attribute needs to be a whole number bigger that 0")
            exit(ErrorCodes.ERR_XML_SYNTAX.value)
        return

    def validate_arguments(self, tag):
        args = getattr(self, "args")
        print(str(args))
        for argument in tag:
            print(argument.tag + " | " + str(argument.attrib))

    def validate_var(self):

        return
    
    def validate_symb(self):

        return

    def validate_label(self):

        return

    def validate_type(self):

        return



# Interactions with frames, function calling #

class Move(Instruction):
    opcode = "move"
    args = {
        "var": None,
        "symb": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class CreateFrame(Instruction):
    opcode = "createframe"
    args = {
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class PushFrame(Instruction):
    opcode = "pushframe"
    args = {
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class PopFrame(Instruction):
    opcode = "popframe"
    args = {
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Defvar(Instruction):
    opcode = "defvar"
    args = {
        "var": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Call(Instruction):
    opcode = "call"
    args = {
        "label": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Return(Instruction):
    opcode = "return"
    args = {
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Interactions with stack  #

class Pushs(Instruction):
    opcode = "pushs"
    args = {
        "symb": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Pops(Instruction):
    opcode = "pops"
    args = {
        "var": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Arithmetical, relations, bool functions  #


class Add(Instruction):
    opcode = "add"
    args = {
        "var": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Sub(Instruction):
    opcode = "sub"
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Mul(Instruction):
    opcode = "mul"
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class IDiv(Instruction):
    opcode = "idiv"
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Relation(Instruction):
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

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
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

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
    args = {
        "var": None,
        "symb": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Stri2Int(Instruction):
    opcode = "stri2int"
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Input/Output  #

class Read(Instruction):
    opcode = "read"
    args = {
        "var": None,
        "type": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Write(Instruction):
    opcode = "write"
    args = {
        "symb": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Interaction with strings  #

class Concat(Instruction):
    opcode = "concat"
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Strlen(Instruction):
    opcode = "strlen"
    args = {
        "var": None,
        "symb": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Getchar(Instruction):
    opcode = "getchar"
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Setchar(Instruction):
    opcode = "setchar"
    args = {
        "var": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Interaction with types  #

class Type(Instruction):
    opcode = "type"
    args = {
        "var": None,
        "symb": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Flow control  #

class Label(Instruction):
    opcode = "label"
    args = {
        "label": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Jump(Instruction):
    opcode = "jump"
    args = {
        "label": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class JumpIfEq(Instruction):
    opcode = "jumpifeq"
    args = {
        "label": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class JumpIfNeq(Instruction):
    opcode = "jumpifneq"
    args = {
        "label": None,
        "symb1": None,
        "symb2": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Exit(Instruction):
    opcode = "exit"
    args = {
        "symb": None
    }

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Debug tools

class DPrint(Instruction):
    opcode = "dprint"
    args = {
        "symb": None
    }

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
