import re

# === Lexer ===
def tokenize(code):
    token_specification = [
        ('FUNC',     r'func'),
        ('RETURN',   r'return'),
        ('IF',       r'if'),
        ('ELSE',     r'else'),
        ('WHILE',    r'while'),
        ('BOOL',     r'true|false'),
        ('TYPE_INT', r'int'),
        ('TYPE_FLOAT', r'float'),
        ('TYPE_STRING', r'string'),
        ('TYPE_BOOL', r'bool'),
        ('NUMBER',   r'\d+(\.\d+)?'), # Integer or decimal
        ('ID',       r'[a-zA-Z_]\w*'),
        ('STRING',   r'"[^"]*"'),
                
        # Comparison operators (order matters - longer patterns first!)
        ('LESS_EQUAL',    r'<='),
        ('GREATER_EQUAL', r'>='),
        ('EQUAL',         r'=='),
        ('NOT_EQUAL',     r'!='),
        ('LESS',          r'<'),
        ('GREATER',       r'>'),

        # Logical operators
        ('AND',     r'&&'),
        ('OR',      r'\|\|'),
        ('NOT',     r'!'),

        # Assignment and arithmetic
        ('ASSIGN',   r'='),
        ('ADD',      r'\+'),
        ('SUB',      r'-'),
        ('MUL',      r'\*'),
        ('DIV',      r'/'),

        # Delimiters
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('COMMA',  r','),
        ('SEMI',   r';'),
        ('SKIP',     r'[ \t]+'),       # Skip spaces
    ]
    tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        match kind:
            case 'NUMBER':
                num = float(value) if '.' in value else int(value)
                tokens.append(('NUMBER', num))
            case 'STRING':
                tokens.append(('STRING', value[1:-1]))
            case 'BOOL':
                tokens.append(('BOOL', value == 'true'))
            case 'SKIP':
                continue
            case _:
                tokens.append((kind, value))
    tokens.append(('EOF', None))
    return tokens
