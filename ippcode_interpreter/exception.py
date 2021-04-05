import enum
import traceback
import sys


__all__ = [
    "ErrorCodes",

    "IPPCodeError",

    "ArgumentsNotValid", "ArgumentsInvalidCombination",

    "XMLParsingError", "InvalidXMLSyntax", "IPPCodeSyntaxError"

    "FileNotFound", "FileRestricted",

    "FrameError", "FrameNotFoundError",

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


class FrameError(IPPCodeError):
    error_msg = "Encountered an exception while trying to interect with a frame"
    exit_code = ErrorCodes.ERR_INTERNAL

    def __init__(self, *args):
        super().__init__(*args)


class FrameNotFoundError(FrameError):
    error_msg = "Selected frame cannot be found in the specified scope"
    exit_code = ErrorCodes.ERR_RUNNING_UNKNOWN_FRAME

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


class FileError(IPPCodeError):
    error_msg = "Encountered an exception while trying to interect with a specified file"
    exit_code = ErrorCodes.ERR_INTERNAL

    def __init__(self, *args):
        super().__init__(*args)


class FileNotFound(FileError):
    error_msg = "Can't open file: No such file or directory"
    exit_code = ErrorCodes.ERR_OPENING_FILES

    def __init__(self, *args):
        super().__init__(*args)


class FileRestricted(FileError):
    error_msg = "Can't write into file: Permisson denied"
    exit_code = ErrorCodes.ERR_WRITING_FILES

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
