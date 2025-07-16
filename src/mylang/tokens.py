from enum import Enum, auto


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()

    # Keywords
    FUNC = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()

    # Types
    INT_TYPE = auto()
    FLOAT_TYPE = auto()
    STRING_TYPE = auto()
    BOOL_TYPE = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()

    # Compound assignment
    FAST_INCREMENT = auto()
    FAST_DECREMENT = auto()
    FAST_ADD_ASSIGN = auto()
    FAST_SUB_ASSIGN = auto()

    # Comparison
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()

    # Delimiters
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()

    # Special
    IDENTIFIER = auto()
    EOF = auto()
    NEWLINE = auto()
    COMMENT_LINE = auto()
    COMMENT_BLOCK = auto()
    SKIP = auto()
