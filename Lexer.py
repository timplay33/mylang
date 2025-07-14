import re

# === Lexer ===
def tokenize(code):
    token_specification = [
        ('FUNC',     r'func'),
        ('RETURN',   r'return'),
        ('NUMBER',   r'\d+(\.\d+)?'), # Integer or decimal
        ('ID',       r'[a-zA-Z_]\w*'),
        ('STRING',   r'"[^"]*"'),
        ('ASSIGN',   r'='),
        ('ADD',      r'\+'),
        ('SUB',      r'-'),
        ('MUL',      r'\*'),
        ('DIV',      r'/'),
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
        if kind == 'NUMBER':
            num = float(value) if '.' in value else int(value)
            tokens.append(('NUMBER', num))
        elif kind == 'STRING':
            tokens.append(('STRING', value[1:-1]))
        elif kind == 'SKIP':
            continue
        else:
            tokens.append((kind, value))
    tokens.append(('EOF', None))
    return tokens
