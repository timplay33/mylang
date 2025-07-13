import re

# === Lexer ===
def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'), # Integer or decimal
        ('ADD',      r'\+'),
        ('SUB',      r'-'),
        ('MUL',      r'\*'),
        ('DIV',      r'/'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('SKIP',     r'[ \t]+'),       # Skip spaces
    ]
    tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', float(value)))
        elif kind == 'SKIP':
            continue
        else:
            tokens.append((kind, value))
    tokens.append(('EOF', None))
    return tokens
