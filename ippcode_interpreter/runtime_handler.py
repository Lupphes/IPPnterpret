from .memory import Memory
from .exception import VariableTypeError


class RuntimeHandler:
    def __init__(self, user_input, *args, **kwargs): 
        self.mem = Memory(user_input)
   
    def handle_compare(self, instance) -> bool:
        var1, var2 = self.check_if_comparison_allowed(instance)
        if instance.opcode == "jumpifeq":
            return var1 == var2
        else:
            return var1 != var2

    def check_if_comparison_allowed(self, instance) -> (int, int):
        passed_args = instance.run()
        var = self.mem.unpack_memory_values(
            args=passed_args,
            result_key=None,
        )

        if var["first"]["type"] == var["second"]["type"]:
            return var["first"]["value"], var["second"]["value"]
        elif var["first"]["type"] == "nil" or var["second"]["type"] == "nil":
            ret1 = None if var["first"]["value"] == "nil" else var["first"]["value"]
            ret2 = None if var["second"]["value"] == "nil" else var["first"]["value"]
            return ret1, ret2
        else:
            raise VariableTypeError()