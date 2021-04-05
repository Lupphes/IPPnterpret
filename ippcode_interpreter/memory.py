from .exception import FrameNotFoundError
from .utils import wrap_with_logging


class Memory(dict):
    def __init__(self, *args, **kwargs):
        super(Memory, self).__init__(*args, **kwargs)
        self.update({
            "GF": {

            },
            "LF": []
        })

    def null_handler(self, *args, **kwargs) -> None:
        pass

    def create_temp_frame(self, frame: dict) -> None:
        self["TF"] = frame

    def push_temp_frame(self, *args) -> None:
        if self.get("TF"):
            self["LF"].append(self.pop("TF"))
        else:
            raise FrameNotFoundError()
            pass

    def pop_temp_frame(self, *args) -> None:
        if len(self["LF"]) > 0:
            self["TF"] = self["LF"].pop(-1)
        else:
            raise FrameNotFoundError()

    def define_variable(self, var: dict) -> None:
        if var["scope"] == "TF" and not self.get("TF"):
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
        elif var["scope"] == "LF":
            self["LF"][-1][var["name"]] = var
        else:
            self[var["scope"]][var["name"]] = var
