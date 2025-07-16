from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List


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


@dataclass
class TokenPattern:
    type: TokenType
    pattern: str
    precedence: int = 0  # For operator precedence


# Token configuration - order matters for regex matching
TOKEN_PATTERNS = [
    # Comments (must come before other operators)
    TokenPattern(TokenType.COMMENT_LINE, r'//.*'),
    TokenPattern(TokenType.COMMENT_BLOCK, r'/\*[\s\S]*?\*/'),

    # Keywords
    TokenPattern(TokenType.FUNC, r'func'),
    TokenPattern(TokenType.RETURN, r'return'),
    TokenPattern(TokenType.IF, r'if'),
    TokenPattern(TokenType.ELSE, r'else'),
    TokenPattern(TokenType.WHILE, r'while'),
    TokenPattern(TokenType.BOOLEAN, r'true|false'),

    # Types
    TokenPattern(TokenType.INT_TYPE, r'int'),
    TokenPattern(TokenType.FLOAT_TYPE, r'float'),
    TokenPattern(TokenType.STRING_TYPE, r'string'),
    TokenPattern(TokenType.BOOL_TYPE, r'bool'),

    # Literals
    TokenPattern(TokenType.NUMBER, r'\d+(\.\d+)?'),
    TokenPattern(TokenType.STRING, r'"[^"]*"'),
    TokenPattern(TokenType.IDENTIFIER, r'[a-zA-Z_]\w*'),

    # Comparison operators (order matters - longer patterns first!)
    TokenPattern(TokenType.LESS_EQUAL, r'<='),
    TokenPattern(TokenType.GREATER_EQUAL, r'>='),
    TokenPattern(TokenType.EQUAL, r'=='),
    TokenPattern(TokenType.NOT_EQUAL, r'!='),
    TokenPattern(TokenType.LESS_THAN, r'<'),
    TokenPattern(TokenType.GREATER_THAN, r'>'),

    # Logical operators
    TokenPattern(TokenType.AND, r'&&'),
    TokenPattern(TokenType.OR, r'\|\|'),
    TokenPattern(TokenType.NOT, r'!'),

    # Fast increment/decrement/assignment
    TokenPattern(TokenType.FAST_INCREMENT, r'\+\+'),
    TokenPattern(TokenType.FAST_DECREMENT, r'--'),
    TokenPattern(TokenType.FAST_ADD_ASSIGN, r'\+='),
    TokenPattern(TokenType.FAST_SUB_ASSIGN, r'-='),

    # Basic operators
    TokenPattern(TokenType.ASSIGN, r'='),
    TokenPattern(TokenType.PLUS, r'\+'),
    TokenPattern(TokenType.MINUS, r'-'),
    TokenPattern(TokenType.MULTIPLY, r'\*'),
    TokenPattern(TokenType.DIVIDE, r'/'),

    # Delimiters
    TokenPattern(TokenType.LEFT_PAREN, r'\('),
    TokenPattern(TokenType.RIGHT_PAREN, r'\)'),
    TokenPattern(TokenType.LEFT_BRACE, r'\{'),
    TokenPattern(TokenType.RIGHT_BRACE, r'\}'),
    TokenPattern(TokenType.COMMA, r','),
    TokenPattern(TokenType.SEMICOLON, r';'),

    # Whitespace
    TokenPattern(TokenType.SKIP, r'[ \t]+'),
]

# Mapping from old token strings to new TokenType enum
LEGACY_TOKEN_MAPPING = {
    'FUNC': TokenType.FUNC,
    'RETURN': TokenType.RETURN,
    'IF': TokenType.IF,
    'ELSE': TokenType.ELSE,
    'WHILE': TokenType.WHILE,
    'BOOL': TokenType.BOOLEAN,
    'TYPE_INT': TokenType.INT_TYPE,
    'TYPE_FLOAT': TokenType.FLOAT_TYPE,
    'TYPE_STRING': TokenType.STRING_TYPE,
    'TYPE_BOOL': TokenType.BOOL_TYPE,
    'NUMBER': TokenType.NUMBER,
    'STRING': TokenType.STRING,
    'ID': TokenType.IDENTIFIER,
    'LESS_EQUAL': TokenType.LESS_EQUAL,
    'GREATER_EQUAL': TokenType.GREATER_EQUAL,
    'EQUAL': TokenType.EQUAL,
    'NOT_EQUAL': TokenType.NOT_EQUAL,
    'LESS': TokenType.LESS_THAN,
    'GREATER': TokenType.GREATER_THAN,
    'AND': TokenType.AND,
    'OR': TokenType.OR,
    'NOT': TokenType.NOT,
    'FAST_IN': TokenType.FAST_INCREMENT,
    'FAST_DE': TokenType.FAST_DECREMENT,
    'FAST_ADD': TokenType.FAST_ADD_ASSIGN,
    'FAST_SUB': TokenType.FAST_SUB_ASSIGN,
    'ASSIGN': TokenType.ASSIGN,
    'ADD': TokenType.PLUS,
    'SUB': TokenType.MINUS,
    'MUL': TokenType.MULTIPLY,
    'DIV': TokenType.DIVIDE,
    'LPAREN': TokenType.LEFT_PAREN,
    'RPAREN': TokenType.RIGHT_PAREN,
    'LBRACE': TokenType.LEFT_BRACE,
    'RBRACE': TokenType.RIGHT_BRACE,
    'COMMA': TokenType.COMMA,
    'SEMI': TokenType.SEMICOLON,
    'EOF': TokenType.EOF,
}
