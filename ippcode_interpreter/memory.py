from .exception import FrameNotFoundError
from .utils import wrap_with_logging
import sys
import re
import typing


class Memory(dict):
    def __init__(self, *args, **kwargs):
        super(Memory, self).__init__(*args, **kwargs)
        self.update({
            "GF": {
            },
            "LF": [],
            "stack": []
        })

    def variable_exists(self, var: dict) -> bool:
        self.scope_exists(var)
        if var["scope"] == "LF":
            if self[var["scope"]][-1].get(var["name"]) is None:
                sys.exit(54)
        elif self[var["scope"]].get(var["name"]) is None:  # TF or GF
            sys.exit(54)

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

    def is_variable_initialized(self) -> None:
        pass

    def are_arguments_valid(self, args: dict, two_symbs=True, init_check=True) -> dict:
        self.variable_exists(args["result"])

        if args["first"]["scope"] is not None:
            self.variable_exists(args["first"])
            args["first"]["value"] = self[args["first"]
                                          ["scope"]][args["first"]["name"]]["value"] #TypeError: list indices must be integers or slices, not str
            args["first"]["type"] = self[args["first"]
                                         ["scope"]][args["first"]["name"]]["type"]
            if init_check:
                if args["first"]["type"] == None:
                    sys.exit(56)

        if two_symbs:
            if args["second"]["scope"] is not None:
                self.variable_exists(args["second"])
                args["second"]["value"] = self[args["second"]
                                               ["scope"]][args["second"]["name"]]["value"]
                args["second"]["type"] = self[args["second"]
                                              ["scope"]][args["second"]["name"]]["type"]
        
            if init_check:
                if args["second"]["type"] == typing.Any:
                    sys.exit(56)


        return args

    def null_handler(self, *args, **kwargs) -> None:
        pass

    def create_temp_frame(self, frame: dict) -> None:
        self["TF"] = frame

    def push_temp_frame(self, *args) -> None:
        if "TF" in self:
            self["LF"].append(self.pop("TF"))
        else:
            raise FrameNotFoundError()

    def pop_temp_frame(self, *args) -> None:
        if len(self["LF"]) > 0:
            self["TF"] = self["LF"].pop(-1)
        else:
            raise FrameNotFoundError()

    def define_variable(self, var: dict) -> None:
        self.scope_exists(var)
        if var["scope"] == "LF":
            self["LF"][-1][var["name"]] = {
                "type": var["type"],
                "value": var["value"]
            }
        else:
            self[var["scope"]][var["name"]] = {
                "type": var["type"],
                "value": var["value"]
            }

    def move_variable(self, var: dict) -> None:
        if var["from"]["scope"] is not None:
            self.variable_exists(var["from"])  # variable

        self.variable_exists(var["to"])
        self[var["to"]["scope"]][var["to"]["name"]].update({
            "type": var["from"]["type"],
            "value": var["from"]["value"]
        })

    def write_variable(self, var: dict) -> None:
        if var["scope"] is not None:
            self.variable_exists(var)  # variable
            if var["scope"] == "LF":
                output = self.unpack_character(
                    self[var["scope"]][-1][var["name"]]["value"])
                print(output, end='')
            else:
                output = self.unpack_character(
                    self[var["scope"]][var["name"]]["value"])
                print(output, end='')
        else:
            output = self.unpack_character(var["value"])
            print(output, end='')

    def dprint_handle(self, var: dict) -> None:
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

    def exit_handle(self, var: dict) -> None:
        if var["scope"] is not None:
            self.variable_exists(var)  # variable
            if var["scope"] == "LF":
                exit_value = self[var["scope"]][-1][var["name"]]["value"]
            else:
                exit_value = self[var["scope"]][var["name"]]["value"]
        else:
            exit_value = var["value"]

        if var["type"] == "int" and 0 <= int(exit_value) <= 49:
            sys.exit(int(exit_value))
        else:
            sys.exit(57)

    def break_handle(self, order) -> None:
        print(
            f"Actual state of GF: {self['GF']}\n"
            f"Actual state of LF: {self['LF']}\n"
            f"Active frame in LF: {self['LF'][-1] if len(self['LF']) != 0 else 'LF is empty'}\n"
            f"Actual state of TF: {self['TF'] if 'TF' in self else 'Not initialized'}\n"
            f"Order: {order}",
            file=sys.stderr
        )

    def pushs_hander(self, var: dict) -> None:
        if var["scope"] is not None:  # variable
            self.variable_exists(var)
            var["value"] = self[var["scope"]][var["name"]]["value"]
            var["type"] = self[var["scope"]][var["name"]]["type"]

        self["stack"].append(var)

    def pops_hander(self, var: dict) -> None:
        self.variable_exists(var)
        returned = self["stack"].pop()
        self[var["scope"]][var["name"]]["value"] = returned["value"]
        self[var["scope"]][var["name"]]["type"] = returned["type"]

    def artihmetic_operation(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=True,
            init_check=True
        )
        result = {}
        if var["first"]["type"] == var["second"]["type"] == "int":
            result["type"] = "int"
            if var["opcode"] == "add":
                var["result"]["value"] = int(
                    var["first"]["value"]) + int(var["second"]["value"])
            elif var["opcode"] == "sub":
                var["result"]["value"] = int(
                    var["first"]["value"]) - int(var["second"]["value"])
            elif var["opcode"] == "mul":
                var["result"]["value"] = int(
                    var["first"]["value"]) * int(var["second"]["value"])
            else:
                if int(var["second"]["value"]) != 0:
                    var["result"]["value"] = int(
                        int(var["first"]["value"]) / int(var["second"]["value"]))
                else:
                    sys.exit(57)
        else:
            sys.exit(53)

        result["value"] = str(var["result"]["value"])

        self[var["result"]["scope"]][var["result"]["name"]] = result

    def relational_operation(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=True,
            init_check=True
        )

        result = {}
        result["type"] = "bool"
        if var["first"]["type"] or var["second"]["type"] == "nil":
            if var["opcode"] == "eq":
                var["result"]["value"] = var["first"]["value"] == var["second"]["value"]
            else:
                sys.exit(53)
        else:
            if var["opcode"] == "lt":
                var["result"]["value"] = var["first"]["value"] < var["second"]["value"]
            elif var["opcode"] == "gt":
                var["result"]["value"] = var["first"]["value"] > var["second"]["value"]
            elif var["opcode"] == "eq":
                var["result"]["value"] = var["first"]["value"] == var["second"]["value"]

        var["result"]["value"] = "true" if var["result"] == True else "false"

        result["value"] = var["result"]["value"]

        self[var["result"]["scope"]][var["result"]["name"]] = result

        print(var)

    def logic_operation(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=True,
            init_check=True
        )

        result = {}
        result["type"] = "bool"
        if var["first"]["type"] or var["second"]["type"] == "nil":
            sys.exit(53)
        else:
            if var["opcode"] == "AND":
                result["value"] = "true" if var["first"]["value"] and var["second"]["value"] == True else "false"
            elif var["opcode"] == "OR":
                result["value"] = "true" if var["first"]["value"] or var["second"]["value"] == True else "false"

        self[var["result"]["scope"]][var["result"]["name"]] = result

    def not_operation(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=False,
            init_check=True
        )

        result = {}
        result["type"] = "bool"
        if var["first"]["type"] or var["second"]["type"] == "nil":
            sys.exit(53)
        else:
            result["value"] = "true" if not var["first"]["value"] == True else "false"

        self[var["result"]["scope"]][var["result"]["name"]] = result

    def int_to_char_handle(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=False,
            init_check=True
        )

        result = {}
        if var["first"]["type"] == "int":
            result["type"] = "string"
            if 0 <= int(var["first"]["value"]) <= 0x10FFFF:
                result["value"] = chr(int(var["first"]["value"]))
            else:
                sys.exit(58)
        else:
            sys.exit(53)

        self[var["result"]["scope"]][var["result"]["name"]] = result

    def string_to_int_handle(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=True,
            init_check=True
        )

        result = {}
        if var["first"]["type"] == "string" and var["second"]["type"] == "int":
            result["type"] = "int"
            if 0 <= var["second"]["value"] <= len(var["first"]["value"]):
                result["value"] = ord(
                    var["first"]["value"][int(var["first"]["second"])])
            else:
                sys.exit(58)
        else:
            sys.exit(53)

        self[var["result"]["scope"]][var["result"]["name"]] = result

    def concat_handler(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=True,
            init_check=True
        )
        result = {}
        if var["first"]["type"] == var["second"]["type"] == "string":
            result["type"] = "string"
            result["value"] = str(var["first"]["value"]) + str(var["second"]["value"])
        else:
            sys.exit(53)

        self[var["result"]["scope"]][var["result"]["name"]] = result

    def strlen_handler(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=False,
            init_check=True
        )

        result = {}
        if var["first"]["type"] == "string":
            result["type"] = "int"
            result["value"] = len(var["first"]["value"])
        else:
            sys.exit(53)

        self[var["result"]["scope"]][var["result"]["name"]] = result

    def getchar_handler(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=True,
            init_check=True
        )

        result = {}
        if var["first"]["type"] == "string" and var["second"]["type"] == "int":
            result["type"] = "string"
            if 0 <= int(var["second"]["value"]) < len(var["first"]["value"]):
                result["value"] = var["first"]["value"][int(var["second"]["value"])]
            else:
                sys.exit(58)
        else:
            sys.exit(53)

        self[var["result"]["scope"]][var["result"]["name"]] = result

    def setchar_handler(self, passed_args: dict) -> None:
        var = self.are_arguments_valid(
            args=passed_args,
            two_symbs=True,
            init_check=True
        )

        result = {}
        if var["result"]["type"] == var["first"]["type"] == "string" and var["first"]["type"] == "int":
            result["type"] = "string"
            if 0 <= var["first"]["value"] <= len(var["result"]["value"]):
                result["value"] = var["result"]["value"][:var["first"]["value"]] + \
                    var["second"]["value"][0] + \
                    var["result"]["value"][var["first"]["value"]+1:]
            else:
                sys.exit(58)
        else:
            sys.exit(53)

    def type_hander(self, var: dict) -> None:
        pass

    def read_hander(self, var: dict) -> None:
        pass
