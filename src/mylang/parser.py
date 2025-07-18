from .ast import *
from .tokens import TokenType
from .lexer import Token
from .error import SyntaxError
from typing import List, Optional

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        """Get the current token"""
        if self.pos >= len(self.tokens):
            # Return EOF token with location if we're past the end
            return self.tokens[-1] if self.tokens else Token(TokenType.EOF, None, SourceLocation(1, 1))
        return self.tokens[self.pos]

    def peek(self) -> TokenType:
        """Peek at the current token type"""
        return self.current_token().type

    def peek_location(self) -> SourceLocation:
        """Get the location of the current token"""
        return self.current_token().location

    def advance(self):
        """Move to the next token"""
        self.pos += 1

    def match(self, expected: TokenType):
        """Match and consume a token of the expected type"""
        token = self.current_token()
        if token.type == expected:
            self.advance()
            return token.value
        raise SyntaxError(
            f'Expected {expected.name} but got {token.type.name} ({token.value!r})',
            token.location)

    def _token_to_string(self, token_type: TokenType) -> str:
        """Convert TokenType to string for operators"""
        mapping = {
            TokenType.PLUS: '+',
            TokenType.MINUS: '-',
            TokenType.MULTIPLY: '*',
            TokenType.DIVIDE: '/',
            TokenType.EQUAL: '==',
            TokenType.NOT_EQUAL: '!=',
            TokenType.LESS_THAN: '<',
            TokenType.GREATER_THAN: '>',
            TokenType.LESS_EQUAL: '<=',
            TokenType.GREATER_EQUAL: '>=',
            TokenType.AND: '&&',
            TokenType.OR: '||',
            TokenType.NOT: '!',
        }
        return mapping.get(token_type, str(token_type))

    def parse(self) -> Program:
        """Parse the token stream into an AST"""
        statements = []
        start_location = self.peek_location() if self.tokens else SourceLocation(1, 1)
        
        while self.pos < len(self.tokens) and self.peek() != TokenType.EOF:
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        
        return Program(statements, start_location)

    def statement(self) -> Optional[Statement]:
        """Parse a statement"""
        location = self.peek_location()
        
        match self.peek():
            case TokenType.FUNC:
                return self.function_declaration()
            case TokenType.RETURN:
                self.match(TokenType.RETURN)
                expr = self.expr()
                self.match(TokenType.SEMICOLON)
                return ReturnStatement(expr, location)
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
                return ExpressionStatement(expr, location)

    # expr -> comparison
    def expr(self) -> Expression:
        return self.logical_or()

    # logical_or -> logical_and (|| logical_and)*
    def logical_or(self) -> Expression:
        node = self.logical_and()
        while self.peek() in (TokenType.OR,):
            location = self.peek_location()
            op_token = self.peek()
            self.advance()
            right = self.logical_and()
            node = BinaryOp(node, self._token_to_string(op_token), right, location)
        return node

    # logical_and -> equality (&& equality)*
    def logical_and(self) -> Expression:
        node = self.equality()
        while self.peek() in (TokenType.AND,):
            location = self.peek_location()
            op_token = self.peek()
            self.advance()
            right = self.equality()
            node = BinaryOp(node, self._token_to_string(op_token), right, location)
        return node

    # equality -> comparison ((==|!=) comparison)*
    def equality(self) -> Expression:
        node = self.comparison()
        while self.peek() in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            location = self.peek_location()
            op_token = self.peek()
            self.advance()
            right = self.comparison()
            node = BinaryOp(node, self._token_to_string(op_token), right, location)
        return node

    # comparison -> addition ((<|>|<=|>=) addition)*
    def comparison(self) -> Expression:
        node = self.addition()
        while self.peek() in (TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            location = self.peek_location()
            op_token = self.peek()
            self.advance()
            right = self.addition()
            node = BinaryOp(node, self._token_to_string(op_token), right, location)
        return node

    # addition -> term ((+|-) term)*
    def addition(self) -> Expression:
        node = self.term()
        while self.peek() in (TokenType.PLUS, TokenType.MINUS):
            location = self.peek_location()
            op_token = self.peek()
            self.advance()
            right = self.term()
            node = BinaryOp(node, self._token_to_string(op_token), right, location)
        return node

    # term -> factor ((*|/) factor)*
    def term(self) -> Expression:
        node = self.unary()
        while self.peek() in (TokenType.MULTIPLY, TokenType.DIVIDE):
            location = self.peek_location()
            op_token = self.peek()
            self.advance()
            right = self.unary()
            node = BinaryOp(node, self._token_to_string(op_token), right, location)
        return node

    def unary(self) -> Expression:
        if self.peek() in (TokenType.NOT, TokenType.MINUS):
            location = self.peek_location()
            op_token = self.peek()
            self.advance()
            node = self.unary()  # Recursive call for nested unary operators
            return UnaryOp(self._token_to_string(op_token), node, location)
        else:
            return self.factor()

    # factor -> NUMBER | (expr)
    def factor(self) -> Expression:
        location = self.peek_location()
        
        match self.peek():
            case TokenType.NUMBER:
                value = self.match(TokenType.NUMBER)
                return Literal(value, location=location)
            case TokenType.BOOLEAN:
                value = self.match(TokenType.BOOLEAN)
                return Literal(value, location=location)
            case TokenType.STRING:
                value = self.match(TokenType.STRING)
                return Literal(value, location=location)
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
                    return FunctionCall(name, args, location)
                else:
                    return Variable(name, location)
            case TokenType.LEFT_PAREN:
                self.match(TokenType.LEFT_PAREN)
                node = self.expr()
                self.match(TokenType.RIGHT_PAREN)
                return node
            case _:
                token = self.current_token()
                raise SyntaxError(f"Unexpected token: {token.type.name} ({token.value!r})", token.location)

    def variable_declaration(self) -> Declaration:
        location = self.peek_location()
        type_token = self.match(self.peek())
        name = self.match(TokenType.IDENTIFIER)
        expr = None
        if self.peek() == TokenType.ASSIGN:
            self.match(TokenType.ASSIGN)
            expr = self.expr()
        self.match(TokenType.SEMICOLON)
        return Declaration(type_token, name, expr, location)

    def function_declaration(self) -> FunctionDeclaration:
        location = self.peek_location()
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
        return FunctionDeclaration(name, params, body, ret_type, location)

    def if_statement(self) -> IfStatement:
        location = self.peek_location()
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
            return IfStatement(condition, body, else_body, location)
        return IfStatement(condition, body, location=location)

    def while_statement(self) -> WhileStatement:
        location = self.peek_location()
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
        return WhileStatement(condition, body, location)

    def assignment_or_expression_statement(self) -> Statement:
        location = self.peek_location()
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
                return ExpressionStatement(FunctionCall(name, args, location), location)
            case TokenType.ASSIGN:
                self.match(TokenType.ASSIGN)
                expr = self.expr()
                self.match(TokenType.SEMICOLON)
                return Assignment(name, expr, location)
            case TokenType.FAST_INCREMENT | TokenType.FAST_DECREMENT:  # x++; x--;
                op_token = self.peek()
                op = self.match(self.peek())
                self.match(TokenType.SEMICOLON)
                # Convert fast operators to regular arithmetic
                if op_token == TokenType.FAST_INCREMENT:
                    return Assignment(name, BinaryOp(Variable(name, location), '+', Literal(1, location=location), location), location)
                else:  # FAST_DECREMENT
                    return Assignment(name, BinaryOp(Variable(name, location), '-', Literal(1, location=location), location), location)
            case TokenType.FAST_ADD_ASSIGN | TokenType.FAST_SUB_ASSIGN:  # x += 5; -=
                op_token = self.peek()
                op = self.match(self.peek())
                expr = self.expr()
                self.match(TokenType.SEMICOLON)
                # Convert fast assignment operators to regular arithmetic
                if op_token == TokenType.FAST_ADD_ASSIGN:
                    return Assignment(name, BinaryOp(Variable(name, location), '+', expr, location), location)
                else:  # FAST_SUB_ASSIGN
                    return Assignment(name, BinaryOp(Variable(name, location), '-', expr, location), location)
            case _:
                self.match(TokenType.SEMICOLON)
                return ExpressionStatement(Variable(name, location), location)
