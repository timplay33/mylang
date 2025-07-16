from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict


class ASTNode(ABC):
    """Base class for all AST nodes"""
    pass


class Expression(ASTNode):
    """Base class for expressions"""
    pass


class Statement(ASTNode):
    """Base class for statements"""
    pass


class Literal(Expression):
    def __init__(self, value: Any, type_hint: Optional[str] = None):
        self.value = value
        self.type_hint = type_hint


class BinaryOp(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOp(Expression):
    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand


class Variable(Expression):
    def __init__(self, name: str):
        self.name = name


class FunctionCall(Expression):
    def __init__(self, name: str, args: List[Expression]):
        self.name = name
        self.args = args


class Declaration(Statement):
    def __init__(self, type_name: str, var_name: str, initializer: Optional[Expression] = None):
        self.type_name = type_name
        self.var_name = var_name
        self.initializer = initializer


class Assignment(Statement):
    def __init__(self, var_name: str, value: Expression):
        self.var_name = var_name
        self.value = value


class IfStatement(Statement):
    def __init__(self, condition: Expression, then_branch: List[Statement], else_branch: Optional[List[Statement]] = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body


class FunctionDeclaration(Statement):
    def __init__(self, name: str, params: List[tuple], body: List[Statement], return_type: Optional[str] = None):
        self.name = name
        self.params = params
        self.body = body
        self.return_type = return_type


class ReturnStatement(Statement):
    def __init__(self, value: Optional[Expression] = None):
        self.value = value


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression


class Program(ASTNode):
    def __init__(self, statements: List[Statement]):
        self.statements = statements
