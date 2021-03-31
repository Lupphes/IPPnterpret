import enum

class ErrorCodes(enum.Enum):
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