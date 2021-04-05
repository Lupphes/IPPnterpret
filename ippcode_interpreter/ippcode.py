import xml.etree.ElementTree as ET
from .parser import Parser
from .memory import Memory
from .utils import wrap_with_logging


class IPPCode21:
    """ Main function of the interpret, creates the code structure and evaluate it """

    def __init__(self, source, input):
        parsed_code = Parser(source, input)
        code_string = "@wrap_with_logging\ndef main():\n"

        resources = {
            "memory": Memory(),
            "wrap_with_logging": wrap_with_logging
        }

        for mangled in parsed_code.mangled_instructions:
            key, instruction = list(mangled.items())[0]
            resources[key] = instruction
            code_string += f"    memory.{instruction.handler_function}({key}.run())\n"

        code_string += "main()"

        exec(code_string, resources)
