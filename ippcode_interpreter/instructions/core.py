import xml.etree.ElementTree as ET
from ..exception import ErrorCodes
from ..parser import Parser
import re


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
        if len(args) != len(tag):
            print("Number of arguments for this instruction doesn't match")
            exit(ErrorCodes.ERR_XML_SYNTAX.value)

        for argument in tag:
            arg_reg = re.compile(r"(^arg)(\d+$)")
            arg_number = arg_reg.match(argument.tag).groups()
            if arg_number[0] == "arg" and arg_number[1] is not None:
                if not argument.attrib["type"]:
                    print("Type is not in the arguments")
                    exit(ErrorCodes.ERR_XML_SYNTAX.value)
                index = int(arg_number[1])-1
                if args[index]:
                    Instruction.validate_atribute_values(
                        argument.attrib["type"], "" if (argument.text is None) else argument.text, args[index]["name"])
                    args[index]["type"] = argument.attrib["type"]
                    args[index]["value"] = argument.text
                else:
                    print("Argument has wrong value")
                    exit(ErrorCodes.ERR_XML_SYNTAX.value)
            else:
                print("Tag has to be names 'arg' with trailing number")
                exit(ErrorCodes.ERR_XML_SYNTAX.value)
        return

    @staticmethod
    def validate_atribute_values(type_attrib, value_attrib, name):
        regexType = {
            "label": r"^[a-zA-Z_\-$!?&%*][a-zA-Z0-9]*",
            "type": r"^string|int|bool$",
            "var": r"^(G|L|T)F@[a-zA-Z_\-$!?&%*][a-zA-Z0-9]*",

            "int": r"^[-+]?[0-9]+$",
            "bool": r"^(true|false)$",
            "string": r"^([^\\#\s]|(\\\d\d\d))*$",
            "nil": r"^nil$"
        }
        constant_literal = ["int", "string", "bool"]
        arg_reg = False


        if name == "label" and type_attrib.lower() == "label":
            arg_reg = re.compile(regexType[type_attrib])
        elif name == "type" and type_attrib.lower() == "type":
            arg_reg = re.compile(regexType[type_attrib])
        elif name == "var" and type_attrib.lower() == "var":
            arg_reg = re.compile(regexType[type_attrib])
        elif name == "symb" and type_attrib.lower() == "var":
            Instruction.validate_atribute_values("var", value_attrib, "var")
            return
        elif name == "symb" and type_attrib.lower() == "nil":
            arg_reg = re.compile(regexType[type_attrib])
        elif name == "symb" and type_attrib.lower() in constant_literal:
            if type_attrib in regexType:
                arg_reg = re.compile(regexType[type_attrib])

        if arg_reg and arg_reg.match(value_attrib):
            return

        print("Argument is not specified correctly")
        exit(ErrorCodes.ERR_XML_SYNTAX.value)
        return


# Interactions with frames, function calling #

class Move(Instruction):
    opcode = "move"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class CreateFrame(Instruction):
    opcode = "createframe"
    args = [
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class PushFrame(Instruction):
    opcode = "pushframe"
    args = [
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class PopFrame(Instruction):
    opcode = "popframe"
    args = [
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Defvar(Instruction):
    opcode = "defvar"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Call(Instruction):
    opcode = "call"
    args = [
        {
            "name": "label",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Return(Instruction):
    opcode = "return"
    args = [
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Interactions with stack  #

class Pushs(Instruction):
    opcode = "pushs"
    args = [
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Pops(Instruction):
    opcode = "pops"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)

# Arithmetical, relations, bool functions  #


class Add(Instruction):
    opcode = "add"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Sub(Instruction):
    opcode = "sub"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Mul(Instruction):
    opcode = "mul"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class IDiv(Instruction):
    opcode = "idiv"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Relation(Instruction):
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

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
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

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


class NOT(Instruction):
    opcode = "not"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Int2Char(Instruction):
    opcode = "int2char"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Stri2Int(Instruction):
    opcode = "stri2int"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Input/Output  #

class Read(Instruction):
    opcode = "read"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "type",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Write(Instruction):
    opcode = "write"
    args = [
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Interaction with strings  #

class Concat(Instruction):
    opcode = "concat"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Strlen(Instruction):
    opcode = "strlen"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Getchar(Instruction):
    opcode = "getchar"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Setchar(Instruction):
    opcode = "setchar"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Interaction with types  #

class Type(Instruction):
    opcode = "type"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Flow control  #

class Label(Instruction):
    opcode = "label"
    args = [
        {
            "name": "label",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Jump(Instruction):
    opcode = "jump"
    args = [
        {
            "name": "label",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class JumpIfEq(Instruction):
    opcode = "jumpifeq"
    args = [
        {
            "name": "label",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class JumpIfNeq(Instruction):
    opcode = "jumpifneq"
    args = [
        {
            "name": "label",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        },
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Exit(Instruction):
    opcode = "exit"
    args = [
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


# Debug tools

class DPrint(Instruction):
    opcode = "dprint"
    args = [
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self):
        return

    @classmethod
    def run(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)


class Break(Instruction):
    opcode = "break"
    args = [
    ]

    def __init__(self):
        return

    @classmethod
    def create(cls, *args, **kwargs):
        # do something
        return cls(*args, **kwargs)
