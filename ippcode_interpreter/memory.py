import typing
import re
import sys
from .utils import wrap_with_logging
from .exception import (
    FrameNotFoundError, UndefinedVariableError, VariableRedefinitionError, 
    VariableIsNotInitializedError, VariableTypeError, 
    IndexOutOfRangeError, DivisionByZeroError, OperandError, MissingValueOnStackError
    )


class Memory(dict):
    def __init__(self, user_input, *args, **kwargs):
        super(Memory, self).__init__(*args, **kwargs)
        self.update({
            "GF": {
            },
            "LF": [],
            "stack": [],
            "stdin": user_input,
            "input_set": False if user_input else True,
            "help_var1": None,
            "help_var2": None
        })

    def variable_exists(self, var: dict) -> bool:
        self.scope_exists(var)
        if var["scope"] == "LF":
            if self[var["scope"]][-1].get(var["name"]) is None:
                raise UndefinedVariableError()
        elif self[var["scope"]].get(var["name"]) is None:  # TF or GF
            raise UndefinedVariableError()

    def scope_exists(self, var: dict) -> bool:
        if var["scope"] == "TF" and self.get("TF") is None:
            raise FrameNotFoundError(
                "The TF frame was not initialised; use CREATE_FRAME to initialise it"
            )
        elif var["scope"] == "LF" and len(self["LF"]) == 0:
            if self.get("TF"):
                raise FrameNotFoundError(
                    "The LF stack is empty; push TF into stack"
                )
            else:
                raise FrameNotFoundError(
                    "The LF stack is empty; initialise TF and push it into the stack"
                )

    def unpack_character(self, string: str) -> str:
        regex_unicode = r"(\\\d\d\d)"
        res_str = re.split(regex_unicode, str(string))
        if len(res_str) == 1:
            return string
        result = ""
        for part in res_str:
            if re.match(regex_unicode, part):
                part = chr(int(part[1:]))
            result += part
        return result

    def is_variable_initialized(self, var: dict) -> None:
        if var["type"] is None and var["value"] is None:
            raise VariableIsNotInitializedError()

    def unpack_memory_values(self, args: dict, result_key="result", check_key=["first", "second"], init_check=True) -> dict:
        if result_key is not None:
            self.variable_exists(args[result_key])

        for key in check_key:
            if args[key]["scope"] is not None:
                self.variable_exists(args[key])
                if args[key]["scope"] == "LF":
                    args[key]["value"] = self[args[key]
                                              ["scope"]][-1][args[key]["name"]]["value"]
                    args[key]["type"] = self[args[key]
                                             ["scope"]][-1][args[key]["name"]]["type"]
                else:
                    args[key]["value"] = self[args[key]
                                              ["scope"]][args[key]["name"]]["value"]
                    args[key]["type"] = self[args[key]
                                             ["scope"]][args[key]["name"]]["type"]
                if init_check:
                    self.is_variable_initialized(args[key])
            elif args[key]["type"] is not None and args[key]["value"] is None:
                args[key]["value"] = ""
            elif args[key]["type"] == "int":
                args[key]["value"] = int(args[key]["value"])
            elif args[key]["type"] == "bool":
                args[key]["value"] = True if args[key]["value"] == "true" else False
            elif args[key]["type"] == "string":
                args[key]["value"] = self.unpack_character(args[key]["value"])

        return args

    def write_memory_values(self, var: dict, result_var: dict) -> None:
        if var["result"]["scope"] == "LF":
            self[var["result"]["scope"]][-1][var["result"]["name"]] = result_var
        else:
            self[var["result"]["scope"]][var["result"]["name"]] = result_var

    def null_handler(self, *args, **kwargs) -> None:
        pass

    # Interactions with frames, function calling

    def move_handler(self, passed_args: dict) -> None:
        args = self.unpack_memory_values(passed_args, "result", ["first"])

        result = {
            "type": passed_args["first"]["type"],
            "value": passed_args["first"]["value"]
        }

        self.write_memory_values(var=args, result_var=result)

    def create_frame_handler(self, frame: dict) -> None:
        self["TF"] = frame

    def push_frame_handler(self, *args) -> None:
        if "TF" in self:
            self["LF"].append(self.pop("TF"))
        else:
            raise FrameNotFoundError()

    def pop_frame_handler(self, *args) -> None:
        if len(self["LF"]) > 0:
            self["TF"] = self["LF"].pop(-1)
        else:
            raise FrameNotFoundError()

    def defvar_handler(self, var: dict) -> None:
        self.scope_exists(var)
        if var["scope"] == "LF":
            if self[var["scope"]][-1].get(var["name"]) is not None:
                raise VariableRedefinitionError()
            else:
                self["LF"][-1][var["name"]] = {
                    "type": var["type"],
                    "value": var["value"]
                }
        elif self[var["scope"]].get(var["name"]) is not None:  # TF or GF
            raise VariableRedefinitionError()
        else:
            self[var["scope"]][var["name"]] = {
                "type": var["type"],
                "value": var["value"]
            }

    # Interactions with stack

    def pushs_handler(self, passed_args: dict) -> None:
        args = self.unpack_memory_values(
            {"first": passed_args}, None, ["first"])
        result = {
            "value": args["first"]["value"],
            "type": args["first"]["type"]
        }
        self["stack"].append(result)

    def pops_handler(self, var: dict) -> None:
        self.variable_exists(var)
        if self["stack"]:
            returned = self["stack"].pop()
        else:
            raise MissingValueOnStackError()
        self[var["scope"]][var["name"]]["value"] = returned["value"]
        self[var["scope"]][var["name"]]["type"] = returned["type"]

    # Arithmetical, relations, bool functions

    def artihmetic_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args
        )
        result = {}
        if var["first"]["type"] == var["second"]["type"] == "int":
            result["type"] = "int"
            if passed_args["opcode"] == "add":
                var["result"]["value"] = var["first"]["value"] + \
                    var["second"]["value"]
            elif passed_args["opcode"] == "sub":
                var["result"]["value"] = var["first"]["value"] - \
                    var["second"]["value"]
            elif passed_args["opcode"] == "mul":
                var["result"]["value"] = var["first"]["value"] * \
                    var["second"]["value"]
            else:
                if var["second"]["value"] != 0:
                    var["result"]["value"] = int(
                        var["first"]["value"] / var["second"]["value"])
                else:
                    raise DivisionByZeroError()
        else:
            raise VariableTypeError()

        result["value"] = var["result"]["value"]

        self.write_memory_values(var=var, result_var=result)

    def relational_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args
        )

        result = {}
        result["type"] = "bool"

        if var["first"]["type"] == "nil" or var["second"]["type"] == "nil":
            if passed_args["opcode"] == "eq":
                var["result"]["value"] = var["first"]["value"] == var["second"]["value"]
            else:
                raise VariableTypeError()
        elif var["first"]["type"] == var["second"]["type"]:
            if passed_args["opcode"] == "lt":
                var["result"]["value"] = var["first"]["value"] < var["second"]["value"]
            elif passed_args["opcode"] == "gt":
                var["result"]["value"] = var["first"]["value"] > var["second"]["value"]
            elif passed_args["opcode"] == "eq":
                var["result"]["value"] = var["first"]["value"] == var["second"]["value"]
        else:
            raise VariableTypeError()

        result["value"] = var["result"]["value"]

        self.write_memory_values(var=var, result_var=result)

    def logic_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args
        )

        result = {}
        result["type"] = "bool"
        if var["first"]["type"] == var["second"]["type"] == "bool":
            if passed_args["opcode"] == "and":
                result["value"] = var["first"]["value"] and var["second"]["value"]
            else:  # or
                result["value"] = var["first"]["value"] or var["second"]["value"]
        else:
            raise VariableTypeError()

        self.write_memory_values(var=var, result_var=result)

    def not_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args,
            check_key=["first"]
        )

        result = {}
        result["type"] = "bool"
        if var["first"]["type"] == "bool":
            result["value"] = not var["first"]["value"]
        else:
            raise VariableTypeError()

        self.write_memory_values(var=var, result_var=result)

    def int_to_char_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args,
            check_key=["first"]
        )

        result = {}
        if var["first"]["type"] == "int":
            result["type"] = "string"
            if 0 <= var["first"]["value"] <= 0x10FFFF:
                result["value"] = chr(var["first"]["value"])
            else:
                raise IndexOutOfRangeError()
        else:
            raise VariableTypeError()

        self.write_memory_values(var=var, result_var=result)

    def string_to_int_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args
        )

        result = {}
        if var["first"]["type"] == "string" and var["second"]["type"] == "int":
            result["type"] = "int"
            if 0 <= var["second"]["value"] < len(var["first"]["value"]):
                result["value"] = ord(
                    var["first"]["value"][var["second"]["value"]])
            else:
                raise IndexOutOfRangeError()
        else:
            raise VariableTypeError()

        self.write_memory_values(var=var, result_var=result)

    # Input/Output

    def read_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args,
            result_key="result",
            check_key=[]
        )
        result = {}
        if self["input_set"]:
            out = input()
            if out == "":
                result["value"] = "nil"
                result["type"] = "nil"
                self.write_memory_values(var=var, result_var=result)
                return
        else:
            if not self["stdin"]:
                result["value"] = "nil"
                result["type"] = "nil"
                self.write_memory_values(var=var, result_var=result)
                return
            else:
                out = self["stdin"].pop()

        if var["first"]["value"] == "int":
            try:
                result["value"] = int(out)
                result["type"] = var["first"]["value"]
            except ValueError:
                result["value"] = "nil"
                result["type"] = "nil"
        elif var["first"]["value"] == "string":
            result["value"] = out
            result["type"] = var["first"]["value"]
        else:  # bool
            if out.lower() == "true":
                result["value"] = True
            else:
                result["value"] = False
            result["type"] = var["first"]["value"]

        self.write_memory_values(var=var, result_var=result)

    def write_handler(self, var: dict) -> None:
        args = self.unpack_memory_values({"first": var}, None, ["first"])

        if args["first"]["type"] == "bool":
            args["first"]["value"] = "true" if args["first"]["value"] else "false"
        elif args["first"]["type"] == "nil":
            args["first"]["value"] = ""

        output = args["first"]["value"]
        print(output, end='')

    # Interaction with strings

    def concat_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args
        )
        result = {}
        if var["first"]["type"] == var["second"]["type"] == "string":
            result["type"] = "string"
            result["value"] = var["first"]["value"] + var["second"]["value"]
        else:
            raise VariableTypeError()

        self.write_memory_values(var=var, result_var=result)

    def strlen_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args,
            check_key=["first"]
        )

        result = {}
        if var["first"]["type"] == "string":
            result["type"] = "int"
            if var["first"]["value"] is None:
                result["value"] = 0
            else:
                result["value"] = len(var["first"]["value"])
        else:
            raise VariableTypeError()

        self.write_memory_values(var=var, result_var=result)

    def getchar_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args
        )

        result = {}
        if var["first"]["type"] == "string" and var["second"]["type"] == "int":
            result["type"] = "string"
            if 0 <= var["second"]["value"] < len(var["first"]["value"]):
                result["value"] = var["first"]["value"][var["second"]["value"]]
            else:
                raise IndexOutOfRangeError()
        else:
            raise VariableTypeError()

        self.write_memory_values(var=var, result_var=result)

    def setchar_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args,
            check_key=["first", "second", "result"]
        )

        result = {}
        if var["first"]["type"] == "int" and var["second"]["type"] == "string" and var["result"]["type"] == "string":
            result["type"] = "string"
            if (0 <= var["first"]["value"] < len(var["result"]["value"])) and var["second"]["value"] != "":
                result["value"] = var["result"]["value"][:var["first"]["value"]] + \
                    var["second"]["value"][0] + \
                    var["result"]["value"][var["first"]["value"]+1:]
            else:
                raise IndexOutOfRangeError()
        else:
            raise VariableTypeError()

        self.write_memory_values(var=var, result_var=result)

    def type_handler(self, passed_args: dict) -> None:
        var = self.unpack_memory_values(
            args=passed_args,
            result_key="result",
            check_key=["first"],
            init_check=False
        )

        result = {}
        result["type"] = "string"

        if var["first"]["type"] is None and var["first"]["value"] is None:
            result["value"] = ""
        else:
            result["value"] = var["first"]["type"]

        self.write_memory_values(var=var, result_var=result)

    def exit_handler(self, var: dict) -> None:
        self.unpack_memory_values({"first": var}, None, ["first"])
        if var["scope"] is not None:
            self.variable_exists(var)  # variable
            if var["scope"] == "LF":
                exit_value = self[var["scope"]][-1][var["name"]]["value"]
            else:
                exit_value = self[var["scope"]][var["name"]]["value"]
        else:
            exit_value = var["value"]

        if var["type"] == "int":
            if 0 <= int(exit_value) <= 49:
                sys.exit(int(exit_value))
            else:
                raise OperandError()
        else:
            raise VariableTypeError()

    # Debug tools

    def dprint_handler(self, var: dict) -> None:
        if var["scope"] is not None:
            self.variable_exists(var)  # variable
            if var["scope"] == "LF":
                print(self[var["scope"]][-1][var["name"]]
                      ["value"], file=sys.stderr)
            else:
                print(self[var["scope"]][var["name"]]
                      ["value"], file=sys.stderr)
        else:
            print(var["value"], file=sys.stderr)

    def break_handler(self, order) -> None:
        print(
            f"Actual state of GF: {self['GF']}\n"
            f"Actual state of LF: {self['LF']}\n"
            f"Active frame in LF: {self['LF'][-1] if len(self['LF']) != 0 else 'LF is empty'}\n"
            f"Actual state of TF: {self['TF'] if 'TF' in self else 'Not initialized'}\n"
            f"Order: {order}",
            file=sys.stderr
        )
