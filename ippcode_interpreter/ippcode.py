import xml.etree.ElementTree as ET
from .parser import Parser
from .memory import Memory
from .utils import wrap_with_logging
from .exception import LabelDoesNotExists, MissingValueOnStackError, FileRestrictedError


class IPPCode21:
    """ Main function of the interpret, creates the code structure and executes it """

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
        saved_index = {}
        indent_level = "    "
        indent_counter = 1
        was_here = False
        jumped_over = []

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
                    if not instance in saved_index: 
                        code_string += indent_level + f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                        was_here = False
                        if return_position or jumped_over and jumped_over[-1] > index:
                            if instance.opcode == "jumpifneq":
                                code_string += indent_level + "while memory['help_var1'] != memory['help_var2']:\n"
                            else:
                                code_string += indent_level + "while memory['help_var1'] == memory['help_var2']:\n"
                        else:
                            if instance.opcode == "jumpifneq":
                                code_string += indent_level + "if memory['help_var1'] != memory['help_var2']:\n"
                            else:
                                code_string += indent_level + "if memory['help_var1'] == memory['help_var2']:\n"

                        indent_level += "    "
                        saved_index[instance] = {
                            "index": index, 
                            "counter": indent_counter,
                            "indent_level": indent_level
                        }
                        
                        indent_counter += 1
                        resources[instance.mangled_name] = instance
                        index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                    else:
                        code_string += indent_level + f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                        index = saved_index[instance]["index"]
                        indent_counter -= 1
                             
                        if was_here:
                            indent_level = saved_index[instance]["indent_level"]
                            code_string += indent_level[:-4] + "else:\n"
                        else:
                            code_string += indent_level[:-4] + "else:\n"
                            was_here = True
                        saved_index.pop(instance)  
                else:
                    raise LabelDoesNotExists()
                index += 1
            elif instance.opcode == "call":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    return_position.append(index)
                    index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                    if jumped_over:
                        jumped_over.pop()
                else:
                    raise LabelDoesNotExists()
                index += 1
            elif instance.opcode == "return":
                if return_position:
                    jumped_over.append(index)
                    index = return_position.pop() + 1
                else:
                    raise MissingValueOnStackError(
                        "RETURN was executed without CALL"
                        )
            else:
                resources[instance.mangled_name] = instance
                code_string += indent_level + f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                index += 1
                if instance.opcode == "exit":
                    break
            if index >= parsed_code.program_length and saved_index:
                max_index = max(saved_index.items(), key=lambda x: x[1]["counter"])
                index = max_index[1]["index"]

        code_string += indent_level + "pass\n"
        if code_string == header:
            code_string += "    pass\n"
        code_string += "main()"
        exec(code_string, resources)

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
