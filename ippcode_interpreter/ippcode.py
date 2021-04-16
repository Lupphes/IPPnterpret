import xml.etree.ElementTree as ET
from .parser import Parser
from .memory import Memory
from .utils import wrap_with_logging
from .exception import LabelDoesNotExists, MissingValueOnStackError, FileRestrictedError
from .runtime_handler import RuntimeHandler


class IPPCode21:
    """ Main function of the interpret, creates the code structure and executes it """

    def __init__(self, source, user_input):
        parsed_code = Parser(source)
        content = self.open_file(user_input)

        resources = {
            "rth": RuntimeHandler(content),
            "wrap_with_logging": wrap_with_logging
        }
        
        index = 0
        return_position = []
        while index < parsed_code.program_length:
            instance = parsed_code.mangled_instructions["instructions"][index]
            if instance is None or instance.opcode == "label":
                index += 1
            elif instance.opcode == "jump":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                else:
                    raise LabelDoesNotExists()
            elif instance.opcode == "jumpifeq" or instance.opcode == "jumpifneq":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    var1, var2 = resources["rth"].check_if_comparison_allowed(instance)
                    if instance.opcode == "jumpifeq":
                        if var1 == var2:
                            index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                        else:
                            index += 1
                    else:
                        if var1 != var2:
                            index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                        else:
                            index += 1
                else:
                    raise LabelDoesNotExists()
            elif instance.opcode == "call":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    return_position.append(index)
                    index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                else:
                    raise LabelDoesNotExists()
            elif instance.opcode == "return":
                if return_position:
                    index = return_position.pop()
                    index += 1
                else:
                    raise MissingValueOnStackError(
                        "RETURN was executed without CALL"
                    )
            else:
                resources[instance.mangled_name] = instance
                eval(f"rth.mem.{instance.handler_function}({instance.mangled_name}.run())", resources)
                # print(resources["rth"].mem)
                index += 1

    def open_file(self, user_input: str) -> str:
        """ Opens file and loads memory """
        if user_input is None:
            return None
        try:
            with open(user_input, 'r') as f:
                file_cont = f.read().splitlines()
        except IOError:
            raise FileRestrictedError()

        return file_cont[::-1]
