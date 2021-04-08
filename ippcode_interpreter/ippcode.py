import xml.etree.ElementTree as ET
from .parser import Parser
from .memory import Memory
from .utils import wrap_with_logging
import sys


class IPPCode21:
    """ Main function of the interpret, creates the code structure and evaluate it """

    def __init__(self, source, user_input):
        parsed_code = Parser(source)
        content = self.open_file(user_input)

        active_label = "@"
        resources = {
            "memory": Memory(content),
            "wrap_with_logging": wrap_with_logging
        }
        header = "@wrap_with_logging\ndef main():\n"
        code_string = header
        
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
                    sys.exit(-1)
                else:
                    sys.exit(52)
                index += 1
            elif instance.opcode == "jumpifneq":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    sys.exit(-1)
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
                    parsed_code.mangled_instructions["instructions"].pop(index)
                    parsed_code.program_length -=  1
                    index = return_position.pop() + 1
                else:
                    sys.exit(56)
            else:
                resources[instance.mangled_name] = instance
                code_string += f"    memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                index += 1


        if code_string == header:
            code_string += "    pass\n"
        code_string += "main()"
        exec(code_string, resources)

    def open_file(self, user_input: str) -> str:
        if user_input is None:
            return None
        with open(user_input, 'r') as f:
            file_cont = f.read().splitlines()

        return file_cont[::-1]
