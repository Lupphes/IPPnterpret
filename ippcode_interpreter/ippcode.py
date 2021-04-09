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
        saved_index = []
        indent_level = "    "

        index = 0
        return_position = []
        while index < parsed_code.program_length:
            instance = parsed_code.mangled_instructions["instructions"][index]
            if instance is None:
                index += 1
                continue
            elif instance.opcode == "label":
                index += 1
            elif instance.opcode == "jump":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                else:
                    sys.exit(52)
            elif instance.opcode == "jumpifeq" or instance.opcode == "jumpifneq":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    if not saved_index:
                        code_string += indent_level
                        code_string += f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"

                        code_string += indent_level
                        if instance.opcode == "jumpifneq":
                            code_string += "while memory['help_var1'] != memory['help_var2']:\n"
                        else:
                            code_string += "while memory['help_var1'] == memory['help_var2']:\n"
                        indent_level += "    "

                        saved_index.append(index)
                        resources[instance.mangled_name] = instance
                        index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                    else:
                        code_string += indent_level
                        code_string += f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                        index = saved_index.pop()
                        indent_level = indent_level[:-4]
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
                    sys.exit(56)
            else:
                resources[instance.mangled_name] = instance
                code_string += indent_level
                code_string += f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                index += 1
                if instance.opcode == "exit":
                    break

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
