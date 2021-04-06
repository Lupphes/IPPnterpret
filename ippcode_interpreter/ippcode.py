import xml.etree.ElementTree as ET
from .parser import Parser
from .memory import Memory
from .utils import wrap_with_logging
import sys


class IPPCode21:
    """ Main function of the interpret, creates the code structure and evaluate it """

    def __init__(self, source, input):
        parsed_code = Parser(source, input)

        active_label = "@"
        resources = {
            "memory": Memory(),
            "wrap_with_logging": wrap_with_logging
        }

        code_string = "@wrap_with_logging\ndef main():\n"
        index = 0
        return_position = []
        while index < parsed_code.program_length:
            instance = parsed_code.mangled_instructions["instructions"][index]

            if instance.opcode == "label":
                index += 1
            elif instance.opcode == "jump":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                else:
                    sys.exit(52)
            elif instance.opcode == "jumpifeq":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    # print(resources["memory"]["jump_value"])
                    pass
                else:
                    sys.exit(52)
                index += 1
            elif instance.opcode == "jumpifneq":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    pass
                else:
                    sys.exit(52)
                index += 1
            elif instance.opcode == "call":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    return_position.append(index)
                    index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                else:
                    sys.exit(52)
                index += 1
            elif instance.opcode == "return":
                if return_position:
                    index = return_position.pop() + 1
                else:
                    sys.exit(55)
            else:
                resources[instance.mangled_name] = instance
                code_string += f"    memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                index += 1
                

        code_string += "main()"
        exec(code_string, resources)
