import re
from .tokens import TokenType
from .error import SourceLocation
from typing import List, Tuple, Any, Optional

# === Lexer ===

class Token:
    """Token with source location information"""
    def __init__(self, token_type: TokenType, value: Any, location: SourceLocation):
        self.type = token_type
        self.value = value
        self.location = location
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.location})"

def tokenize(code: str, filename: Optional[str] = None) -> List[Token]:
    token_specification = [
        # Comments (must come before other operators)
        (TokenType.COMMENT_LINE,  r'//.*'),           # Line comment
        (TokenType.COMMENT_BLOCK, r'/\*[\s\S]*?\*/'),      # Block comment

        # Keywords
        (TokenType.FUNC,     r'func'),
        (TokenType.RETURN,   r'return'),
        (TokenType.IF,       r'if'),
        (TokenType.ELSE,     r'else'),
        (TokenType.WHILE,    r'while'),
        (TokenType.BOOLEAN,  r'true|false'),
        
        # Types
        (TokenType.INT_TYPE, r'int'),
        (TokenType.FLOAT_TYPE, r'float'),
        (TokenType.STRING_TYPE, r'string'),
        (TokenType.BOOL_TYPE, r'bool'),
        
        # Literals
        (TokenType.NUMBER,   r'\d+(\.\d+)?'),  # Integer or decimal
        (TokenType.IDENTIFIER, r'[a-zA-Z_]\w*'),
        (TokenType.STRING,   r'"[^"]*"'),

        # Comparison operators (order matters - longer patterns first!)
        (TokenType.LESS_EQUAL,    r'<='),
        (TokenType.GREATER_EQUAL, r'>='),
        (TokenType.EQUAL,         r'=='),
        (TokenType.NOT_EQUAL,     r'!='),
        (TokenType.LESS_THAN,     r'<'),
        (TokenType.GREATER_THAN,  r'>'),

        # Logical operators
        (TokenType.AND,     r'&&'),
        (TokenType.OR,      r'\|\|'),
        (TokenType.NOT,     r'!'),

        # Fast increment/decrement/assignment
        (TokenType.FAST_INCREMENT, r'\+\+'),
        (TokenType.FAST_DECREMENT, r'--'),
        (TokenType.FAST_ADD_ASSIGN, r'\+='),
        (TokenType.FAST_SUB_ASSIGN, r'-='),

        # Assignment and arithmetic
        (TokenType.ASSIGN,   r'='),
        (TokenType.PLUS,     r'\+'),
        (TokenType.MINUS,    r'-'),
        (TokenType.MULTIPLY, r'\*'),
        (TokenType.DIVIDE,   r'/'),

        # Delimiters
        (TokenType.LEFT_PAREN,   r'\('),
        (TokenType.RIGHT_PAREN,  r'\)'),
        (TokenType.LEFT_BRACE,   r'\{'),
        (TokenType.RIGHT_BRACE,  r'\}'),
        (TokenType.COMMA,        r','),
        (TokenType.SEMICOLON,    r';'),
        (TokenType.SKIP,         r'[ \t]+'),       # Skip spaces
        (TokenType.NEWLINE,      r'\n'),           # Newlines for position tracking
    ]
    
    tok_regex = '|'.join(
        f'(?P<{token_type.name}>{regex})' for token_type, regex in token_specification)
    tokens = []
    
    line = 1
    line_start = 0
    
    for mo in re.finditer(tok_regex, code):
        kind_name = mo.lastgroup
        value = mo.group()
        start_pos = mo.start()
        
        if kind_name is None:
            continue
            
        kind = TokenType[kind_name]
        
        # Handle newlines for position tracking
        if kind == TokenType.NEWLINE:
            line += 1
            line_start = mo.end()
            continue  # Don't include newlines in token stream
        
        # Calculate line and column
        column = start_pos - line_start + 1
        location = SourceLocation(line, column, filename)
        
        if kind == TokenType.NUMBER:
            num = float(value) if '.' in value else int(value)
            tokens.append(Token(kind, num, location))
        elif kind == TokenType.STRING:
            tokens.append(Token(kind, value[1:-1], location))
        elif kind == TokenType.BOOLEAN:
            tokens.append(Token(kind, value == 'true', location))
        elif kind in (TokenType.COMMENT_LINE, TokenType.COMMENT_BLOCK, TokenType.SKIP):
            continue
        else:
            tokens.append(Token(kind, value, location))
    
    # Add EOF token at the end of the file
    final_location = SourceLocation(line, len(code) - line_start + 1 if tokens else 1, filename)
    tokens.append(Token(TokenType.EOF, None, final_location))
    return tokens
