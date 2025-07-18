class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos >= len(self.tokens):
            return 'EOF'
        return self.tokens[self.pos][0]

    def advance(self):
        self.pos += 1

    def match(self, expected):
        if self.peek() == expected:
            val = self.tokens[self.pos][1]
            self.advance()
            return val
        token = self.tokens[self.pos] if self.pos < len(
            self.tokens) else ('EOF', '')
        raise SyntaxError(
            f'expected: {expected} but got: {token[0]} ({token[1]!r}) at position {self.pos}')

    def parse(self):
        statements = []
        while self.pos < len(self.tokens) and self.peek() != 'EOF':
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def statement(self):
        match self.peek():
            case 'FUNC':
                return self.function_declaration()
            case 'RETURN':
                self.match('RETURN')
                expr = self.expr()
                self.match('SEMI')
                return ('return', expr)
            case 'TYPE_INT' | 'TYPE_FLOAT' | 'TYPE_STRING' | 'TYPE_BOOL':
                return self.variable_declaration()
            case 'IF':
                return self.if_statement()
            case 'WHILE':
                return self.while_statement()
            case 'ID':
                return self.assignment_or_expression_statement()
            case 'EOF':
                return None
            case _:
                expr = self.expr()
                self.match('SEMI')
                return ('expr_stmt', expr)

    # expr -> comparison
    def expr(self):
        return self.logical_or()

    # logical_or -> logical_and (|| logical_and)*
    def logical_or(self):
        node = self.logical_and()
        while self.peek() in ('OR',):
            op = self.match(self.peek())
            right = self.logical_and()
            node = (op, node, right)
        return node

    # logical_and -> equality (&& equality)*
    def logical_and(self):
        node = self.equality()
        while self.peek() in ('AND',):
            op = self.match(self.peek())
            right = self.equality()
            node = (op, node, right)
        return node

    # equality -> comparison ((==|!=) comparison)*
    def equality(self):
        node = self.comparison()
        while self.peek() in ('EQUAL', 'NOT_EQUAL'):
            op = self.match(self.peek())
            right = self.comparison()
            node = (op, node, right)
        return node

    # comparison -> addition ((<|>|<=|>=) addition)*
    def comparison(self):
        node = self.addition()
        while self.peek() in ('LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL'):
            op = self.match(self.peek())
            right = self.addition()
            node = (op, node, right)
        return node

    # addition -> term ((+|-) term)*
    def addition(self):
        node = self.term()
        while self.peek() in ('ADD', 'SUB'):
            op = self.match(self.peek())
            right = self.term()
            node = (op, node, right)
        return node

    # term -> factor ((*|/) factor)*
    def term(self):
        node = self.unary()
        while self.peek() in ('MUL', 'DIV'):
            op = self.match(self.peek())
            right = self.unary()
            node = (op, node, right)
        return node

    def unary(self):
        if self.peek() in ('NOT', 'SUB'):
            op = self.match(self.peek())
            node = self.unary()  # Recursive call for nested unary operators
            return (op, node)
        else:
            return self.factor()

    # factor -> NUMBER | (expr)
    def factor(self):
        match self.peek():
            case 'NUMBER':
                return self.match('NUMBER')
            case 'BOOL':
                return self.match('BOOL')
            case 'STRING':
                return self.match('STRING')
            case 'ID':
                name = self.match('ID')
                if self.peek() == 'LPAREN':  # Function Call
                    self.match('LPAREN')
                    args = []
                    if self.peek() != 'RPAREN':
                        args.append(self.expr())
                        while self.peek() == 'COMMA':
                            self.match('COMMA')
                            args.append(self.expr())
                    self.match('RPAREN')
                    return ('call', name, args)
                else:
                    return ('var', name)
            case 'LPAREN':
                self.match('LPAREN')
                node = self.expr()
                self.match('RPAREN')
                return node
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

    def function_declaration(self):
        self.match('FUNC')
        ret_type = self.match(self.peek())
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
            stmt = self.statement()
            if stmt is not None:
                body.append(stmt)
        self.match('RBRACE')
        return ('func', name, params, body, ret_type)

    def if_statement(self):
        self.match('IF')
        self.match('LPAREN')
        condition = self.expr()
        self.match('RPAREN')
        self.match('LBRACE')
        body = []
        while self.peek() != 'RBRACE':
            stmt = self.statement()
            if stmt is not None:
                body.append(stmt)
        self.match('RBRACE')
        if self.peek() == 'ELSE':
            self.match('ELSE')
            self.match('LBRACE')
            else_body = []
            while self.peek() != 'RBRACE':
                stmt = self.statement()
                if stmt is not None:
                    else_body.append(stmt)
            self.match('RBRACE')
            return ('if', condition, body, else_body)
        return ('if', condition, body)

    def while_statement(self):
        self.match('WHILE')
        self.match('LPAREN')
        condition = self.expr()
        self.match('RPAREN')
        self.match('LBRACE')
        body = []
        while self.peek() != 'RBRACE':
            stmt = self.statement()
            if stmt is not None:
                body.append(stmt)
        self.match('RBRACE')
        return ('while', condition, body)

    def assignment_or_expression_statement(self):
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
                return ('expr_stmt', ('call', name, args))
            case 'ASSIGN':
                self.match('ASSIGN')
                expr = self.expr()
                self.match('SEMI')
                return ('assign', name, expr)
            case 'FAST_IN' | 'FAST_DE':  # x++; x--;
                op = self.match(self.peek())[0]
                self.match('SEMI')
                return ('assign', name, (op, ('var', name), 1))
            case 'FAST_ADD' | 'FAST_SUB':  # x += 5; -=
                op = self.match(self.peek())[0]
                expr = self.expr()
                self.match('SEMI')
                return ('assign', name, (op, ('var', name), expr))
            case _:
                self.match('SEMI')
                return ('expr_stmt', ('var', name))
