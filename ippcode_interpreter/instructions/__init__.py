import sys
import inspect
from . import core
from .core import *
from typing import Tuple, List, Union


def get_class_by_opcode(opcode: str) -> Union[Instruction, None]:
    """ This method creates child-class with specified opcode from the instruction class """
    module_items: List[Tuple[str, object]] = inspect.getmembers(
        sys.modules[core.__name__], inspect.isclass)
    for name, obj in module_items:
        if not name.startswith('_'):
            if getattr(obj, 'opcode', None) == opcode:
                return obj  # Without () so it's just the class
    return None