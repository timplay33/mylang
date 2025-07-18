from abc import ABC
from typing import Any, List, Optional
from .error import SourceLocation


class ASTNode(ABC):
    """Base class for all AST nodes"""
    def __init__(self, location: Optional[SourceLocation] = None):
        self.location = location


class Expression(ASTNode):
    """Base class for expressions"""
    def __init__(self, location: Optional[SourceLocation] = None):
        super().__init__(location)


class Statement(ASTNode):
    """Base class for statements"""
    def __init__(self, location: Optional[SourceLocation] = None):
        super().__init__(location)


class Literal(Expression):
    """AST node for literal values (numbers, strings, booleans)"""
    def __init__(self, value: Any, type_hint: Optional[str] = None, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.value = value
        self.type_hint = type_hint or self._infer_type_hint(value)
    
    def _infer_type_hint(self, value: Any) -> str:
        """Infer type hint from the value"""
        if isinstance(value, bool):  # Check bool before int (bool is subclass of int)
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'string'
        else:
            return 'unknown'


class BinaryOp(Expression):
    """AST node for binary operations (e.g., +, -, *, /, ==, !=)"""
    def __init__(self, left: Expression, operator: str, right: Expression, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOp(Expression):
    """AST node for unary operations (e.g., -, !)"""
    def __init__(self, operator: str, operand: Expression, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.operator = operator
        self.operand = operand


class Variable(Expression):
    """AST node for variable references"""
    def __init__(self, name: str, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.name = name


class FunctionCall(Expression):
    """AST node for function calls"""
    def __init__(self, name: str, args: List[Expression], location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.args = args


class Declaration(Statement):
    """AST node for variable declarations (e.g., int x = 5;)"""
    def __init__(self, type_name: str, var_name: str, initializer: Optional[Expression] = None, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.type_name = type_name
        self.var_name = var_name
        self.initializer = initializer


class Assignment(Statement):
    """AST node for variable assignments (e.g., x = 10;)"""
    def __init__(self, var_name: str, value: Expression, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.var_name = var_name
        self.value = value


class IfStatement(Statement):
    """AST node for if statements with optional else branch"""
    def __init__(self, condition: Expression, then_branch: List[Statement], else_branch: Optional[List[Statement]] = None, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStatement(Statement):
    """AST node for while loops"""
    def __init__(self, condition: Expression, body: List[Statement], location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.condition = condition
        self.body = body


class FunctionDeclaration(Statement):
    """AST node for function declarations"""
    def __init__(self, name: str, params: List[tuple], body: List[Statement], return_type: Optional[str] = None, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.params = params
        self.body = body
        self.return_type = return_type


class ReturnStatement(Statement):
    """AST node for return statements"""
    def __init__(self, value: Optional[Expression] = None, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.value = value


class ExpressionStatement(Statement):
    """AST node for expression statements (expressions used as statements)"""
    def __init__(self, expression: Expression, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.expression = expression


class Program(ASTNode):
    """Root AST node representing the entire program"""
    def __init__(self, statements: List[Statement], location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.statements = statements
