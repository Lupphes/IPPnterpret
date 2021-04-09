import enum
import traceback
import sys


__all__ = [
    "ErrorCodes",

    "IPPCodeError",

    "ArgumentsNotValid", "ArgumentsInvalidCombination",

    "XMLParsingError", "InvalidXMLSyntax", "IPPCodeSyntaxError"

    "FileError", "FileNotFoundError", "FileRestrictedError",

    "SemanticError", "FrameNotFoundError", "LabelDoesNotExists", "MissingValueOnStackError",
    "UndefinedVariableError", "VariableRedefinitionError", "VariableIsNotInitializedError",
    "VariableTypeError", "DivisionByZeroError", "IndexOutOfRangeError", "OperandError",

    "IPPRuntimeError"
]


class ErrorCodes(enum.IntEnum):
    SUCCESS = 0
    ERR_ARGUMENT_PARSE_COMBINATION = 10
    ERR_OPENING_FILES = 11
    ERR_WRITING_FILES = 12
    ERR_XML_SYNTAX = 31
    ERR_XML_UNEXPECTED_STRUCT = 32
    ERR_SEMANTIC = 52
    ERR_RUNNING_TYPE = 53
    ERR_RUNNING_UNKNOWN_VAR = 54
    ERR_RUNNING_UNKNOWN_FRAME = 55
    ERR_RUNNING_MISSING_VAL = 56
    ERR_RUNNING_OPERAND = 57
    ERR_RUNNING_STRING = 58
    ERR_INTERNAL = 99


class IPPCodeError(Exception):
    error_msg = "IPPCode21 interpreter encoutered an exception"
    exit_code = ErrorCodes.ERR_INTERNAL

    def __init__(self, *args):
        if args:
            self.error_msg = args[0]
        super().__init__(self.error_msg)
        self.log_exception()
        exit(self.exit_code)

    def log_exception(self):
        print(
            f"Encountered an error while runtime: {self.__class__.__name__}, {self.error_msg}")


class ArgumentsNotValid(IPPCodeError):
    error_msg = "Specified arguments are unrecognized"
    exit_code = ErrorCodes.ERR_ARGUMENT_PARSE_COMBINATION

    def __init__(self, *args):
        super().__init__(*args)


class ArgumentsInvalidCombination(ArgumentsNotValid):
    error_msg = "Specified combination of arguments is not valid"
    exit_code = ErrorCodes.ERR_ARGUMENT_PARSE_COMBINATION

    def __init__(self, *args):
        super().__init__(*args)


class XMLParsingError(IPPCodeError):
    error_msg = "XML parser encoutered a fatal error"
    exit_code = ErrorCodes.ERR_INTERNAL

    def __init__(self, *args):
        super().__init__(*args)


class InvalidXMLSyntax(XMLParsingError):
    error_msg = "XML parser had encountered an invalid syntax"
    exit_code = ErrorCodes.ERR_XML_SYNTAX

    def __init__(self, *args):
        super().__init__(*args)


class IPPCodeSyntaxError(InvalidXMLSyntax):
    error_msg = "XML representation of IPPCode21 is not valid"
    exit_code = ErrorCodes.ERR_XML_UNEXPECTED_STRUCT

    def __init__(self, *args):
        super().__init__(*args)


class FileError(IPPCodeError):
    error_msg = "Encountered an exception while trying to interect with a specified file"
    exit_code = ErrorCodes.ERR_INTERNAL

    def __init__(self, *args):
        super().__init__(*args)


class FileNotFoundError(FileError):
    error_msg = "Can't open file: No such file or directory"
    exit_code = ErrorCodes.ERR_OPENING_FILES

    def __init__(self, *args):
        super().__init__(*args)


class FileRestrictedError(FileError):
    error_msg = "Can't write into file: Permisson denied"
    exit_code = ErrorCodes.ERR_WRITING_FILES

    def __init__(self, *args):
        super().__init__(*args)


class SemanticError(IPPCodeError):
    error_msg = "The code has unknown semantic error"
    exit_code = ErrorCodes.ERR_INTERNAL

    def __init__(self, *args):
        super().__init__(*args)


class FrameNotFoundError(SemanticError):
    error_msg = "Selected frame cannot be found in the specified scope"
    exit_code = ErrorCodes.ERR_RUNNING_UNKNOWN_FRAME

    def __init__(self, *args):
        super().__init__(*args)


class LabelDoesNotExists(SemanticError):
    error_msg = "Can't jump or call to specified label"
    exit_code = ErrorCodes.ERR_SEMANTIC

    def __init__(self, *args):
        super().__init__(*args)


class MissingValueOnStackError(SemanticError):
    error_msg = "The interpret tries to get undefined value on stack"
    exit_code = ErrorCodes.ERR_RUNNING_MISSING_VAL

    def __init__(self, *args):
        super().__init__(*args)


class UndefinedVariableError(SemanticError):
    error_msg = "The variable is not defined in selected scope"
    exit_code = ErrorCodes.ERR_RUNNING_UNKNOWN_VAR

    def __init__(self, *args):
        super().__init__(*args)


class VariableRedefinitionError(SemanticError):
    error_msg = "The specified variable is already defined"
    exit_code = ErrorCodes.ERR_SEMANTIC

    def __init__(self, *args):
        super().__init__(*args)


class VariableIsNotInitializedError(SemanticError):
    error_msg = "The selected variable is not initialized to execute this action"
    exit_code = ErrorCodes.ERR_RUNNING_MISSING_VAL

    def __init__(self, *args):
        super().__init__(*args)


class VariableTypeError(SemanticError):
    error_msg = "The specified type is not compatible with this instruction"
    exit_code = ErrorCodes.ERR_RUNNING_TYPE

    def __init__(self, *args):
        super().__init__(*args)


class DivisionByZeroError(SemanticError):
    error_msg = "Found division by zero"
    exit_code = ErrorCodes.ERR_RUNNING_OPERAND

    def __init__(self, *args):
        super().__init__(*args)


class OperandError(SemanticError):
    error_msg = "The specified operand is not correct in this context"
    exit_code = ErrorCodes.ERR_RUNNING_OPERAND

    def __init__(self, *args):
        super().__init__(*args)


class IndexOutOfRangeError(SemanticError):
    error_msg = "The specied index is out of range"
    exit_code = ErrorCodes.ERR_RUNNING_STRING

    def __init__(self, *args):
        super().__init__(*args)


class IPPRuntimeError(IPPCodeError):
    error_msg = "IPPCode21 interpreter encoutered an exception while running"
    exit_code = ErrorCodes.ERR_INTERNAL

    def __init__(self, *args):
        super().__init__(*args)

    def log_exception(self):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_str = "".join(frame for frame in tb)
        print(f"{tb_str}\n IPPCode21 interpreter encoutered an exception while running; {self.__class__.__name__} => {self.error_msg}")
