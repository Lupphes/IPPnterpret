import xml.etree.ElementTree as ET
from ..exception import IPPCodeSyntaxError
from ..parser import Parser
import re
import typing
from ..utils import wrap_with_logging


class Instruction:
    def __init__(self, tag: ET.Element):
        self.tag = tag
        self.order = int(tag.attrib["order"])
        return

    def validate_arguments(self, tag: ET.Element) -> None:
        args = getattr(self, "args")
        if len(args) != len(tag):
            raise IPPCodeSyntaxError(
                "Number of arguments for this instruction doesn't match"
            )

        for argument in tag:
            arg_reg = re.compile(r"(^arg)(\d+$)")
            arg_number = arg_reg.match(argument.tag)

            if arg_number is None:
                raise IPPCodeSyntaxError(
                    "Tag 'arg' does not have correct syntax"
                )
            arg_number = arg_number.groups()

            if arg_number[0] == "arg" and arg_number[1] is not None:
                if not argument.attrib["type"]:  # Validation of attribute
                    raise IPPCodeSyntaxError("Type is not in the arguments")

                # Indexing the array with this value
                index = int(arg_number[1])-1
                if len(args) > index and index >= 0:  # and fidning if exists
                    self.validate_attribute_values(
                        self,  # Class is not initialized yet due to checking
                        type_attrib=argument.attrib["type"],
                        # The library returns None If text is ""
                        value_attrib="" if argument.text is None else argument.text,
                        name=args[index]["name"]
                    )
                    args[index]["type"] = argument.attrib["type"]
                    args[index]["value"] = argument.text
                else:
                    raise IPPCodeSyntaxError(
                        "Specified argument has wrong value"
                    )
            else:
                raise IPPCodeSyntaxError(
                    "Tag has to be names 'arg' with trailing number"
                )

        return

    def validate_attribute_values(self, type_attrib: str, value_attrib: str, name: str) -> None:
        regexType = {
            "label": r"^[a-zA-Z_\-$!?&%*][a-zA-Z0-9]*",
            "type": r"^(string|int|bool)$",
            "var": r"^(G|L|T)F@[a-zA-Z_\-$!?&%*][a-zA-Z0-9]*",
            "int": r"^[-+]?[0-9]+$",
            "bool": r"^(true|false)$",
            "string": r"^([^\\#\s]|(\\\d\d\d))*$",
            "nil": r"^nil$"
        }

        constant_literal = ["int", "string", "bool"]
        arg_reg = False

        if name == "symb" and type_attrib.lower() == "var":
            type_attrib = "var"
            name = "var"
        if name == "label" and type_attrib.lower() == "label":
            arg_reg = re.compile(regexType[type_attrib])
        elif name == "type" and type_attrib.lower() == "type":
            arg_reg = re.compile(regexType[type_attrib])
        elif name == "var" and type_attrib.lower() == "var":
            arg_reg = re.compile(regexType[type_attrib])
        elif name == "symb" and type_attrib.lower() == "nil":
            arg_reg = re.compile(regexType[type_attrib])
        elif name == "symb" and type_attrib.lower() in constant_literal:
            if type_attrib in regexType:
                arg_reg = re.compile(regexType[type_attrib])

        if arg_reg and arg_reg.match(value_attrib):
            return

        raise IPPCodeSyntaxError("Argument is not specified correctly")
        return

    @classmethod
    def create_mangled_name(cls, order: int) -> str:
        return f"instruction_{cls.__name__.lower()}_{order}"

    def run(self):
        pass

# Interactions with frames, function calling #


class Move(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return


class CreateFrame(Instruction):
    handler_function = "create_temp_frame"
    opcode = "createframe"
    args = [
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return


class PushFrame(Instruction):
    handler_function = "push_temp_frame"
    opcode = "pushframe"
    args = [
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return


class PopFrame(Instruction):
    handler_function = "pop_temp_frame"
    opcode = "popframe"
    args = [
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return


class Defvar(Instruction):
    handler_function = "define_variable"
    opcode = "defvar"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):
        return {
            "scope": self.args[0]["value"].split("@")[0],
            "name": self.args[0]["value"].split("@")[1],
            "type": typing.Any,
            "value": None
        }


class Call(Instruction):
    handler_function = "null_handler"
    opcode = "call"
    args = [
        {
            "name": "label",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Return(Instruction):
    handler_function = "null_handler"
    opcode = "return"
    args = [
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


# Interactions with stack  #

class Pushs(Instruction):
    handler_function = "null_handler"
    opcode = "pushs"
    args = [
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Pops(Instruction):
    handler_function = "null_handler"
    opcode = "pops"
    args = [
        {
            "name": "var",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return

# Arithmetical, relations, bool functions  #


class Add(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Sub(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Mul(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class IDiv(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class LT(Relation):
    handler_function = "null_handler"
    opcode = "lt"

    def __init__(self, tag):
        super().__init__(tag=tag)
        return


class GT(Relation):
    handler_function = "null_handler"
    opcode = "gt"

    def __init__(self, tag):
        super().__init__(tag=tag)
        return


class EQ(Relation):
    handler_function = "null_handler"
    opcode = "eq"

    def __init__(self, tag):
        super().__init__(tag=tag)
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class AND(Logic):
    handler_function = "null_handler"
    opcode = "and"

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class OR(Logic):
    handler_function = "null_handler"
    opcode = "or"

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class NOT(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Int2Char(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Stri2Int(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


# Input/Output  #

class Read(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Write(Instruction):
    handler_function = "null_handler"
    opcode = "write"
    args = [
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


# Interaction with strings  #

class Concat(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Strlen(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Getchar(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Setchar(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


# Interaction with types  #

class Type(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


# Flow control  #

class Label(Instruction):
    handler_function = "null_handler"
    opcode = "label"
    args = [
        {
            "name": "label",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):
        return "It works"


class Jump(Instruction):
    handler_function = "null_handler"
    opcode = "jump"
    args = [
        {
            "name": "label",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class JumpIfEq(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class JumpIfNeq(Instruction):
    handler_function = "null_handler"
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

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


class Exit(Instruction):
    handler_function = "null_handler"
    opcode = "exit"
    args = [
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return


# Debug tools

class DPrint(Instruction):
    handler_function = "null_handler"
    opcode = "dprint"
    args = [
        {
            "name": "symb",
            "value": None,
            "type": None
        }
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):
        print(self.args[0]["value"])
        return


class Break(Instruction):
    handler_function = "null_handler"
    opcode = "break"
    args = [
    ]

    def __init__(self, tag):
        super().__init__(tag=tag)
        return

    def run(self):

        return
