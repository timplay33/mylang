class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos][0]

    def advance(self):
        self.pos += 1

    def match(self, expected):
        if self.peek() == expected:
            val = self.tokens[self.pos][1]
            self.advance()
            return val
        token = self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')
        raise SyntaxError(f'expected: {expected} but got: {token[0]} ({token[1]!r}) at position {self.pos}')

    def parse(self):
        statements = []
        while self.pos < len(self.tokens) and self.peek() != 'EOF':
            expr = self.expr()
            if self.peek() == 'SEMI':
                self.match('SEMI')
            statements.append(expr)
        return statements

    # expr -> term ((+|-) term)*
    def expr(self):
        node = self.term()
        while self.peek() in ('ADD', 'SUB'):
            op = self.match(self.peek())
            right = self.term()
            node = (op, node, right)
        return node

    # term -> factor ((*|/) factor)*
    def term(self):
        node = self.factor()
        while self.peek() in ('MUL', 'DIV'):
            op = self.match(self.peek())
            right = self.factor()
            node = (op, node, right)
        return node

    # factor -> NUMBER | (expr)
    def factor(self):
        match self.peek():
            case 'FUNC':
                self.match('FUNC')
                name = self.match('ID')
                self.match('LPAREN')
                params = []
                if self.peek() != 'RPAREN':
                    params.append((self.match(self.peek()), self.match('ID')))
                    while self.peek() == 'COMMA':
                        self.match('COMMA')
                        params.append((self.match(self.peek()), self.match('ID')))
                self.match('RPAREN')
                self.match('LBRACE')
                body = []
                while self.peek() != 'RBRACE':
                    expr = self.expr()
                    if expr is not None:
                        body.append(expr)
                self.match('RBRACE')
                return ('func', name, params, body)
            case 'RETURN':
                self.match('RETURN')
                expr = self.expr()
                self.match('SEMI')
                return ('return', expr)
            case 'SUB':
                self.match('SUB')
                node = self.factor()
                return ('neg', node)
            case 'NUMBER':
                return self.match('NUMBER')
            case 'BOOL':
                return self.match('BOOL')
            case 'TYPE_INT' | 'TYPE_FLOAT' | 'TYPE_STRING' | 'TYPE_BOOL':
                return self.variable_declaration()
            case 'ID':
                name = self.match('ID')
                match self.peek():
                    case 'LPAREN':
                        self.match('LPAREN')
                        args = []
                        if self.peek() != 'RPAREN':
                            args.append(self.expr())
                            while self.peek() == 'COMMA':
                                self.match('COMMA')
                                args.append(self.expr())
                        self.match('RPAREN')
                        self.match('SEMI')
                        return ('call', name, args)
                    case 'ASSIGN':
                        self.match('ASSIGN')
                        expr = self.expr()
                        self.match('SEMI')
                        return ('assign', name, expr)
                    case _:
                        return ('var', name)
            case 'LPAREN':
                self.match('LPAREN')
                node = self.expr()
                self.match('RPAREN')
                return node
            case 'STRING':
                return self.match('STRING')
            case 'IF':
                self.match('IF')
                self.match('LPAREN')
                condition = self.expr()
                self.match('RPAREN')
                self.match('LBRACE')
                body = []
                while self.peek() != 'RBRACE':
                    body.append(self.expr())
                self.match('RBRACE')
                if self.peek() == 'ELSE':
                    self.match('ELSE')
                    self.match('LBRACE')
                    else_body = []
                    while self.peek() != 'RBRACE':
                        else_body.append(self.expr())
                    self.match('RBRACE')
                    return ('if', condition, body, else_body)
                return ('if', condition, body)
            case 'WHILE':
                self.match('WHILE')
                self.match('LPAREN')
                condition = self.expr()
                self.match('RPAREN')
                self.match('LBRACE')
                body = []
                while self.peek() != 'RBRACE':
                    body.append(self.expr())
                self.match('RBRACE')
                return ('while', condition, body)
            case _:
                raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")
    def variable_declaration(self):
        type_token = self.match(self.peek())
        name = self.match('ID')
        expr = None
        if self.peek() == 'ASSIGN':
            self.match('ASSIGN')
            expr = self.expr()
        self.match('SEMI')
        return ('decl', type_token, name, expr)