import sys
import inspect
from . import core
from .core import *

def get_class_by_opcode(opcode: str):
        module_items = inspect.getmembers(sys.modules[core.__name__], inspect.isclass)
        for name, obj in module_items :
            if not name.startswith('_'):
                if getattr(obj , 'opcode', None) == opcode:
                    return obj # Without () so it's just the class