from .exception import FrameNotFoundError
from .utils import wrap_with_logging
import sys
import re


class Memory(dict):
    def __init__(self, *args, **kwargs):
        super(Memory, self).__init__(*args, **kwargs)
        self.update({
            "GF": {
            },
            "LF": []
            # "@RETURN": None
        })
        self.stack = []

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
        if string is None:
            return ""
        res_str = re.split(regex_unicode, string)
        result = ""
        for part in res_str:
            if re.match(regex_unicode, part):
                part = chr(int(part[1:]))
            result += part
        return result

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
                output = self.unpack_character(self[var["scope"]][-1][var["name"]]["value"])
                print(output, end='')
            else:
                output = self.unpack_character(self[var["scope"]][var["name"]]["value"])
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
