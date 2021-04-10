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
        jumpif_inst = {}
        indent_level = "    "
        indent_counter = 1
        elsed = False
        called_over_if = []
        jumped = []
        break_handler = []

        index = 0
        return_position = []
        while index < parsed_code.program_length:
            instance = parsed_code.mangled_instructions["instructions"][index]
            if instance is None or instance.opcode == "label":
                index += 1
            elif instance.opcode == "jump":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    if parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].end > parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start and index > parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start:
                        if not index in jumped:
                            code_string += indent_level + "while True:\n"
                            indent_level += "    "
                            jumped.append(index)
                            index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                        else:
                            index += 1
                            jumped.pop()
                    else:
                        index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                else:
                    raise LabelDoesNotExists()
            elif instance.opcode == "jumpifeq" or instance.opcode == "jumpifneq":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    if not instance in jumpif_inst:
                        code_string += indent_level + \
                            f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                        elsed = False
                        if return_position or called_over_if and called_over_if[-1] > index:
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
                        jumpif_inst[instance] = {
                            "index": index,
                            "counter": indent_counter,
                            "indent_level": indent_level
                        }

                        indent_counter += 1
                        resources[instance.mangled_name] = instance
                        index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                    else:
                        code_string += indent_level + \
                            f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                        index = jumpif_inst[instance]["index"]
                        indent_counter -= 1

                        if elsed:
                            indent_level = jumpif_inst[instance]["indent_level"]
                            code_string += indent_level[:-4] + "else:\n"
                        else:
                            if jumped:
                                code_string += indent_level + "break\n"
                            code_string += indent_level[:-4] + "else:\n"
                            elsed = True
                        jumpif_inst.pop(instance)
                else:
                    raise LabelDoesNotExists()
                index += 1
            elif instance.opcode == "call":
                if instance.args[0]["value"] in parsed_code.mangled_instructions["labels"]:
                    return_position.append(index)
                    index = parsed_code.mangled_instructions["labels"][instance.args[0]["value"]].start
                    if called_over_if:
                        called_over_if.pop()
                else:
                    raise LabelDoesNotExists()
                index += 1
            elif instance.opcode == "return":
                if return_position:
                    called_over_if.append(index)
                    index = return_position.pop() + 1
                else:
                    raise MissingValueOnStackError(
                        "RETURN was executed without CALL"
                    )
            else:
                resources[instance.mangled_name] = instance
                code_string += indent_level + \
                    f"memory.{instance.handler_function}({instance.mangled_name}.run())\n"
                index += 1
                if instance.opcode == "exit":
                    break
            if index >= parsed_code.program_length and jumpif_inst:
                max_index = max(jumpif_inst.items(),
                                key=lambda x: x[1]["counter"])
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
