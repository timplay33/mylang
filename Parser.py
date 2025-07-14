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
        return None

    def parse(self):
        if self.peek() == 'ID' and self.tokens[self.pos + 1][0] == 'ASSIGN':
            name = self.match('ID')
            self.match('ASSIGN')
            expr = self.expr()
            return ('assign', name, expr)
        else:
            return self.expr()

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
        if self.peek() == 'FUNC':
            self.match('FUNC')
            name = self.match('ID')
            self.match('LPRAEN')
            params = []
            if self.peek() != 'RPAREN':
                params.append(self.match('ID'))
                while self.peek() == 'COMMA':
                    self.match('COMMA')
                    params.append(self.match('ID'))
            self.match('RPAREN')
            self.match('ASSIGN')
            body = self.expr()
            print(name, params, body)
            return ('func', name, params, body) 
        elif self.peek() == 'SUB':
            self.match('SUB')
            node = self.factor()
            return ('neg', node)
        elif self.peek() == 'NUMBER':
            return self.match('NUMBER')
        elif self.peek() == 'ID':
            name = self.match('ID')
            if self.peek() == 'LPAREN':
                self.match('LPAREN')
                args = []
                if self.peek != 'RPAREN':
                    args.append(self.expr())
                    while self.peek() == 'COMMA':
                        self.match('COMMA')
                        args.append(self.expr())
                self.match('RPAREN')
                return ('call', name, args)
            else:
                return ('var', name)
        elif self.peek() == 'LPAREN':
            self.match('LPAREN')
            node = self.expr()
            self.match('RPAREN')
            return node
        elif self.peek() == 'STRING':
            return self.match('STRING') 
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")
