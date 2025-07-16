from .ast import *
from .tokens import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos >= len(self.tokens):
            return TokenType.EOF
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
        while self.pos < len(self.tokens) and self.peek() != TokenType.EOF:
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements)

    def statement(self):
        match self.peek():
            case TokenType.FUNC:
                return self.function_declaration()
            case TokenType.RETURN:
                self.match(TokenType.RETURN)
                expr = self.expr()
                self.match(TokenType.SEMICOLON)
                return ReturnStatement(expr)
            case TokenType.INT_TYPE | TokenType.FLOAT_TYPE | TokenType.STRING_TYPE | TokenType.BOOL_TYPE:
                return self.variable_declaration()
            case TokenType.IF:
                return self.if_statement()
            case TokenType.WHILE:
                return self.while_statement()
            case TokenType.IDENTIFIER:
                return self.assignment_or_expression_statement()
            case TokenType.EOF:
                return None
            case _:
                expr = self.expr()
                self.match(TokenType.SEMICOLON)
                return ExpressionStatement(expr)

    # expr -> comparison
    def expr(self):
        return self.logical_or()

    # logical_or -> logical_and (|| logical_and)*
    def logical_or(self):
        node = self.logical_and()
        while self.peek() in (TokenType.OR,):
            op = self.match(self.peek())
            right = self.logical_and()
            node = BinaryOp(node, op, right)
        return node

    # logical_and -> equality (&& equality)*
    def logical_and(self):
        node = self.equality()
        while self.peek() in (TokenType.AND,):
            op = self.match(self.peek())
            right = self.equality()
            node = BinaryOp(node, op, right)
        return node

    # equality -> comparison ((==|!=) comparison)*
    def equality(self):
        node = self.comparison()
        while self.peek() in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.match(self.peek())
            right = self.comparison()
            node = BinaryOp(node, op, right)
        return node

    # comparison -> addition ((<|>|<=|>=) addition)*
    def comparison(self):
        node = self.addition()
        while self.peek() in (TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.match(self.peek())
            right = self.addition()
            node = BinaryOp(node, op, right)
        return node

    # addition -> term ((+|-) term)*
    def addition(self):
        node = self.term()
        while self.peek() in (TokenType.PLUS, TokenType.MINUS):
            op = self.match(self.peek())
            right = self.term()
            node = BinaryOp(node, op, right)
        return node

    # term -> factor ((*|/) factor)*
    def term(self):
        node = self.unary()
        while self.peek() in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.match(self.peek())
            right = self.unary()
            node = BinaryOp(node, op, right)
        return node

    def unary(self):
        if self.peek() in (TokenType.NOT, TokenType.MINUS):
            op = self.match(self.peek())
            node = self.unary()  # Recursive call for nested unary operators
            return UnaryOp(op, node)
        else:
            return self.factor()

    # factor -> NUMBER | (expr)
    def factor(self):
        match self.peek():
            case TokenType.NUMBER:
                value = self.match(TokenType.NUMBER)
                return Literal(value)
            case TokenType.BOOLEAN:
                value = self.match(TokenType.BOOLEAN)
                return Literal(value)
            case TokenType.STRING:
                value = self.match(TokenType.STRING)
                return Literal(value)
            case TokenType.IDENTIFIER:
                name = self.match(TokenType.IDENTIFIER)
                if self.peek() == TokenType.LEFT_PAREN:  # Function Call
                    self.match(TokenType.LEFT_PAREN)
                    args = []
                    if self.peek() != TokenType.RIGHT_PAREN:
                        args.append(self.expr())
                        while self.peek() == TokenType.COMMA:
                            self.match(TokenType.COMMA)
                            args.append(self.expr())
                    self.match(TokenType.RIGHT_PAREN)
                    return FunctionCall(name, args)
                else:
                    return Variable(name)
            case TokenType.LEFT_PAREN:
                self.match(TokenType.LEFT_PAREN)
                node = self.expr()
                self.match(TokenType.RIGHT_PAREN)
                return node
            case _:
                raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")

    def variable_declaration(self):
        type_token = self.match(self.peek())
        name = self.match(TokenType.IDENTIFIER)
        expr = None
        if self.peek() == TokenType.ASSIGN:
            self.match(TokenType.ASSIGN)
            expr = self.expr()
        self.match(TokenType.SEMICOLON)
        return Declaration(type_token, name, expr)

    def function_declaration(self):
        self.match(TokenType.FUNC)
        ret_type = self.match(self.peek())
        name = self.match(TokenType.IDENTIFIER)
        self.match(TokenType.LEFT_PAREN)
        params = []
        if self.peek() != TokenType.RIGHT_PAREN:
            params.append((self.match(self.peek()), self.match(TokenType.IDENTIFIER)))
            while self.peek() == TokenType.COMMA:
                self.match(TokenType.COMMA)
                params.append((self.match(self.peek()), self.match(TokenType.IDENTIFIER)))
        self.match(TokenType.RIGHT_PAREN)
        self.match(TokenType.LEFT_BRACE)
        body = []
        while self.peek() != TokenType.RIGHT_BRACE:
            stmt = self.statement()
            if stmt is not None:
                body.append(stmt)
        self.match(TokenType.RIGHT_BRACE)
        return FunctionDeclaration(name, params, body, ret_type)

    def if_statement(self):
        self.match(TokenType.IF)
        self.match(TokenType.LEFT_PAREN)
        condition = self.expr()
        self.match(TokenType.RIGHT_PAREN)
        self.match(TokenType.LEFT_BRACE)
        body = []
        while self.peek() != TokenType.RIGHT_BRACE:
            stmt = self.statement()
            if stmt is not None:
                body.append(stmt)
        self.match(TokenType.RIGHT_BRACE)
        if self.peek() == TokenType.ELSE:
            self.match(TokenType.ELSE)
            self.match(TokenType.LEFT_BRACE)
            else_body = []
            while self.peek() != TokenType.RIGHT_BRACE:
                stmt = self.statement()
                if stmt is not None:
                    else_body.append(stmt)
            self.match(TokenType.RIGHT_BRACE)
            return IfStatement(condition, body, else_body)
        return IfStatement(condition, body)

    def while_statement(self):
        self.match(TokenType.WHILE)
        self.match(TokenType.LEFT_PAREN)
        condition = self.expr()
        self.match(TokenType.RIGHT_PAREN)
        self.match(TokenType.LEFT_BRACE)
        body = []
        while self.peek() != TokenType.RIGHT_BRACE:
            stmt = self.statement()
            if stmt is not None:
                body.append(stmt)
        self.match(TokenType.RIGHT_BRACE)
        return WhileStatement(condition, body)

    def assignment_or_expression_statement(self):
        name = self.match(TokenType.IDENTIFIER)
        match self.peek():
            case TokenType.LEFT_PAREN:
                self.match(TokenType.LEFT_PAREN)
                args = []
                if self.peek() != TokenType.RIGHT_PAREN:
                    args.append(self.expr())
                    while self.peek() == TokenType.COMMA:
                        self.match(TokenType.COMMA)
                        args.append(self.expr())
                self.match(TokenType.RIGHT_PAREN)
                self.match(TokenType.SEMICOLON)
                return ExpressionStatement(FunctionCall(name, args))
            case TokenType.ASSIGN:
                self.match(TokenType.ASSIGN)
                expr = self.expr()
                self.match(TokenType.SEMICOLON)
                return Assignment(name, expr)
            case TokenType.FAST_INCREMENT | TokenType.FAST_DECREMENT:  # x++; x--;
                op_token = self.peek()
                op = self.match(self.peek())
                self.match(TokenType.SEMICOLON)
                # Convert fast operators to regular arithmetic - use token type, not value
                if op_token == TokenType.FAST_INCREMENT:
                    return Assignment(name, BinaryOp(Variable(name), TokenType.PLUS, Literal(1)))
                else:  # FAST_DECREMENT
                    return Assignment(name, BinaryOp(Variable(name), TokenType.MINUS, Literal(1)))
            case TokenType.FAST_ADD_ASSIGN | TokenType.FAST_SUB_ASSIGN:  # x += 5; -=
                op_token = self.peek()
                op = self.match(self.peek())
                expr = self.expr()
                self.match(TokenType.SEMICOLON)
                # Convert fast assignment operators to regular arithmetic - use token type, not value
                if op_token == TokenType.FAST_ADD_ASSIGN:
                    return Assignment(name, BinaryOp(Variable(name), TokenType.PLUS, expr))
                else:  # FAST_SUB_ASSIGN
                    return Assignment(name, BinaryOp(Variable(name), TokenType.MINUS, expr))
            case _:
                self.match(TokenType.SEMICOLON)
                return ExpressionStatement(Variable(name))
