import re
from .tokens import TokenType

# === Lexer ===

def tokenize(code):
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
    ]
    
    tok_regex = '|'.join(
        f'(?P<{token_type.name}>{regex})' for token_type, regex in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind_name = mo.lastgroup
        value = mo.group()
        kind = TokenType[kind_name]
        
        if kind == TokenType.NUMBER:
            num = float(value) if '.' in value else int(value)
            tokens.append((kind, num))
        elif kind == TokenType.STRING:
            tokens.append((kind, value[1:-1]))
        elif kind == TokenType.BOOLEAN:
            tokens.append((kind, value == 'true'))
        elif kind in (TokenType.COMMENT_LINE, TokenType.COMMENT_BLOCK, TokenType.SKIP):
            continue
        else:
            tokens.append((kind, value))
    
    tokens.append((TokenType.EOF, None))
    return tokens
