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
        self.validate_arguments(tag)

    @property
    def mangled_name(self) -> str:
        return f"instruction_{self.__class__.__name__.lower()}_{self.order}"

    def validate_arguments(self, tag: ET.Element) -> None:
        self.args = getattr(self, "args")
        if len(self.args) != len(tag):
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
                if len(self.args) > index and index >= 0:  # and finding if exists
                    self.validate_attribute_values(
                        type_attrib=argument.attrib["type"],
                        # The library returns None If text is ""
                        value_attrib="" if argument.text is None else argument.text,
                        name=self.args[index]["name"]
                    )
                    self.args[index]["type"] = argument.attrib["type"]
                    self.args[index]["value"] = argument.text
                else:
                    raise IPPCodeSyntaxError(
                        "Specified argument has wrong value"
                    )
            else:
                raise IPPCodeSyntaxError(
                    "Tag has to be names 'arg' with trailing number"
                )

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

        if not arg_reg or not arg_reg.match(value_attrib):
            raise IPPCodeSyntaxError("Argument is not specified correctly")

    def run(self):
        pass

# Interactions with frames, function calling # Done


class Move(Instruction):
    handler_function = "move_variable"
    opcode = "move"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "from": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1] == "var" else self.args[1]["value"]
            },
            "to": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            }
        }
        return var_move


class CreateFrame(Instruction):
    handler_function = "create_temp_frame"
    opcode = "createframe"

    def __init__(self, tag):
        self.args = []
        super().__init__(tag=tag)

    def run(self):
        return {}


class PushFrame(Instruction):
    handler_function = "push_temp_frame"
    opcode = "pushframe"

    def __init__(self, tag):
        self.args = []
        super().__init__(tag=tag)


class PopFrame(Instruction):
    handler_function = "pop_temp_frame"
    opcode = "popframe"

    def __init__(self, tag):
        self.args = []
        super().__init__(tag=tag)


class Defvar(Instruction):
    handler_function = "define_variable"
    opcode = "defvar"

    def __init__(self, tag):
        self.args = [
            {
                "name": "var",
                "value": None,
                "type": None
            }
        ]
        super().__init__(tag=tag)

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

    def __init__(self, tag):
        self.args = [
            {
                "name": "label",
                "value": None,
                "type": None
            }
        ]
        super().__init__(tag=tag)

    def run(self):

        return


class Return(Instruction):
    handler_function = "null_handler"
    opcode = "return"

    def __init__(self, tag):
        self.args = []
        super().__init__(tag=tag)

    def run(self):

        return


# Interactions with stack  # # Done

class Pushs(Instruction):
    handler_function = "pushs_hander"
    opcode = "pushs"

    def __init__(self, tag):
        self.args = [
            {
                "name": "symb",
                "value": None,
                "type": None
            }
        ]
        super().__init__(tag=tag)

    def run(self):
        return {
            "scope": self.args[0]["value"].split("@")[0] if self.args[0]["type"] == "var" else None,
            "name": self.args[0]["value"].split("@")[1] if self.args[0]["type"] == "var" else None,
            "type": typing.Any if self.args[0]["type"] == "var" else self.args[0]["type"],
            "value": None if self.args[0]["type"] == "var" else self.args[0]["value"]
        }


class Pops(Instruction):
    handler_function = "pops_hander"
    opcode = "pops"

    def __init__(self, tag):
        self.args = [
            {
                "name": "var",
                "value": None,
                "type": None
            }
        ]
        super().__init__(tag=tag)

    def run(self):
        return {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            }

# Arithmetical, relations, bool functions  #


class Arithmetic(Instruction):
    handler_function = "artihmetic_operation"
    def __init__(self, tag):
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            },
            "second": {
                "scope": self.args[2]["value"].split("@")[0] if self.args[2]["type"] == "var" else None,
                "name": self.args[2]["value"].split("@")[1] if self.args[2]["type"] == "var" else None,
                "type": typing.Any if self.args[2]["type"] == "var" else self.args[2]["type"],
                "value": None if self.args[2]["type"] == "var" else self.args[2]["value"]
            }
        }


class Add(Arithmetic):
    opcode = "add"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)


class Sub(Arithmetic):
    opcode = "sub"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)


class Mul(Arithmetic):
    opcode = "mul"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)


class IDiv(Arithmetic):
    opcode = "idiv"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)


class Relational(Instruction):
    handler_function = "relational_operation"
    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            },
            "second": {
                "scope": self.args[2]["value"].split("@")[0] if self.args[2]["type"] == "var" else None,
                "name": self.args[2]["value"].split("@")[1] if self.args[2]["type"] == "var" else None,
                "type": typing.Any if self.args[2]["type"] == "var" else self.args[2]["type"],
                "value": None if self.args[2]["type"] == "var" else self.args[2]["value"]
            }
        }


class LT(Relational):
    opcode = "lt"

    def __init__(self, tag):
        super().__init__(tag=tag)


class GT(Relational):
    opcode = "gt"

    def __init__(self, tag):
        super().__init__(tag=tag)


class EQ(Relational):
    opcode = "  "

    def __init__(self, tag):
        super().__init__(tag=tag)


class Logic(Instruction):
    handler_function = "logic_operation"
    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            },
            "second": {
                "scope": self.args[2]["value"].split("@")[0] if self.args[2]["type"] == "var" else None,
                "name": self.args[2]["value"].split("@")[1] if self.args[2]["type"] == "var" else None,
                "type": typing.Any if self.args[2]["type"] == "var" else self.args[2]["type"],
                "value": None if self.args[2]["type"] == "var" else self.args[2]["value"]
            }
        }


class AND(Logic):
    opcode = "and"

    def __init__(self, tag):
        super().__init__(tag=tag)


class OR(Logic):
    opcode = "or"

    def __init__(self, tag):
        super().__init__(tag=tag)


class NOT(Instruction):
    handler_function = "not_operation"
    opcode = "not"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            }
        }


class Int2Char(Instruction):
    handler_function = "int_to_char_handle"
    opcode = "int2char"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            }
        }


class Stri2Int(Instruction):
    handler_function = "string_to_int_handle"
    opcode = "stri2int"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            },
            "second": {
                "scope": self.args[2]["value"].split("@")[0] if self.args[2]["type"] == "var" else None,
                "name": self.args[2]["value"].split("@")[1] if self.args[2]["type"] == "var" else None,
                "type": typing.Any if self.args[2]["type"] == "var" else self.args[2]["type"],
                "value": None if self.args[2]["type"] == "var" else self.args[2]["value"]
            }
        }


# Input/Output  #

class Read(Instruction):
    handler_function = "read_hander"
    opcode = "read"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "name": self.args[1]["value"],
                "value": None,
                "type": typing.Any
            }
        }


class Write(Instruction):
    handler_function = "write_variable"
    opcode = "write"

    def __init__(self, tag):
        self.args = [
            {
                "name": "symb",
                "value": None,
                "type": None
            }
        ]
        super().__init__(tag=tag)

    def run(self):
        return {
            "scope": self.args[0]["value"].split("@")[0] if self.args[0]["type"] == "var" else None,
            "name": self.args[0]["value"].split("@")[1] if self.args[0]["type"] == "var" else None,
            "type": typing.Any if self.args[0]["type"] == "var" else self.args[0]["type"],
            "value": None if self.args[0]["type"] == "var" else self.args[0]["value"]
        }


# Interaction with strings  #

class Concat(Instruction):
    handler_function = "concat_handler"
    opcode = "concat"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            },
            "second": {
                "scope": self.args[2]["value"].split("@")[0] if self.args[2]["type"] == "var" else None,
                "name": self.args[2]["value"].split("@")[1] if self.args[2]["type"] == "var" else None,
                "type": typing.Any if self.args[2]["type"] == "var" else self.args[2]["type"],
                "value": None if self.args[2]["type"] == "var" else self.args[2]["value"]
            }
        }


class Strlen(Instruction):
    handler_function = "strlen_handler"
    opcode = "strlen"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            }
        }


class Getchar(Instruction):
    handler_function = "getchar_handler"
    opcode = "getchar"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            },
            "second": {
                "scope": self.args[2]["value"].split("@")[0] if self.args[2]["type"] == "var" else None,
                "name": self.args[2]["value"].split("@")[1] if self.args[2]["type"] == "var" else None,
                "type": typing.Any if self.args[2]["type"] == "var" else self.args[2]["type"],
                "value": None if self.args[2]["type"] == "var" else self.args[2]["value"]
            }
        }


class Setchar(Instruction):
    handler_function = "setchar_handler"
    opcode = "setchar"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            },
            "second": {
                "scope": self.args[2]["value"].split("@")[0] if self.args[2]["type"] == "var" else None,
                "name": self.args[2]["value"].split("@")[1] if self.args[2]["type"] == "var" else None,
                "type": typing.Any if self.args[2]["type"] == "var" else self.args[2]["type"],
                "value": None if self.args[2]["type"] == "var" else self.args[2]["value"]
            }
        }


# Interaction with types  #

class Type(Instruction):
    handler_function = "type_hander"
    opcode = "type"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)

    def run(self):
        return {
            "opcode": self.opcode,
            "result": {
                "scope": self.args[0]["value"].split("@")[0],
                "name": self.args[0]["value"].split("@")[1],
                "type": typing.Any,
                "value": None
            },
            "first": {
                "scope": self.args[1]["value"].split("@")[0] if self.args[1]["type"] == "var" else None,
                "name": self.args[1]["value"].split("@")[1] if self.args[1]["type"] == "var" else None,
                "type": typing.Any if self.args[1]["type"] == "var" else self.args[1]["type"],
                "value": None if self.args[1]["type"] == "var" else self.args[1]["value"]
            }
        }


# Flow control  #

class Label(Instruction):
    handler_function = "null_handler"
    opcode = "label"

    def __init__(self, tag):
        self.args = [
            {
                "name": "label",
                "value": None,
                "type": None
            }
        ]
        self.start = None
        self.end = None
        super().__init__(tag=tag)

    def define(self, start: int, end: int) -> None:
        self.start = start
        self.end = end


class Jump(Instruction):
    handler_function = "null_handler"
    opcode = "jump"

    def __init__(self, tag):
        self.args = [
            {
                "name": "label",
                "value": None,
                "type": None
            }
        ]
        super().__init__(tag=tag)


class JumpIfEq(Instruction):
    handler_function = "null_handler"
    opcode = "jumpifeq"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)


class JumpIfNeq(Instruction):
    handler_function = "null_handler"
    opcode = "jumpifneq"

    def __init__(self, tag):
        self.args = [
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
        super().__init__(tag=tag)


class Exit(Instruction):
    handler_function = "exit_handle"
    opcode = "exit"

    def __init__(self, tag):
        self.args = [
            {
                "name": "symb",
                "value": None,
                "type": None
            }
        ]
        super().__init__(tag=tag)

    def run(self):
        return {
            "scope": self.args[0]["value"].split("@")[0] if self.args[0]["type"] == "var" else None,
            "name": self.args[0]["value"].split("@")[1] if self.args[0]["type"] == "var" else None,
            "type": typing.Any if self.args[0]["type"] == "var" else self.args[0]["type"],
            "value": None if self.args[0]["type"] == "var" else self.args[0]["value"]
        }


# Debug tools - Done

class DPrint(Instruction):
    handler_function = "dprint_handle"
    opcode = "dprint"

    def __init__(self, tag):
        self.args = [
            {
                "name": "symb",
                "value": None,
                "type": None
            }
        ]
        super().__init__(tag=tag)

    def run(self):
        return {
            "scope": self.args[0]["value"].split("@")[0] if self.args[0]["type"] == "var" else None,
            "name": self.args[0]["value"].split("@")[1] if self.args[0]["type"] == "var" else None,
            "type": typing.Any if self.args[0]["type"] == "var" else self.args[0]["type"],
            "value": None if self.args[0]["type"] == "var" else self.args[0]["value"]
        }


class Break(Instruction):
    handler_function = "break_handle"
    opcode = "break"

    def __init__(self, tag):
        self.args = []
        super().__init__(tag=tag)

    def run(self):
        return self.order
