from typing import Any, Dict, List, Optional
from .ast import *
from .error import *
from .builtins import BuiltinRegistry
from .tokens import TokenType


class Scope:
    """Represents a variable scope"""

    def __init__(self, parent: Optional['Scope'] = None):
        self.parent = parent
        self.variables: Dict[str, tuple] = {}  # name -> (value, type)

    def define(self, name: str, value: Any, type_name: str):
        """Define a new variable in this scope"""
        if name in self.variables:
            raise EvaluationError(
                f"Variable '{name}' already defined in this scope")
        self.variables[name] = (value, type_name)

    def get(self, name: str) -> tuple:
        """Get a variable from this scope or parent scopes"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise UndefinedVariableError(f"Undefined variable: {name}")

    def set(self, name: str, value: Any):
        """Set a variable in this scope or parent scopes"""
        if name in self.variables:
            old_value, type_name = self.variables[name]
            self.variables[name] = (value, type_name)
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise UndefinedVariableError(f"Undefined variable: {name}")

    def get_type(self, name: str) -> str:
        """Get the type of a variable"""
        _, type_name = self.get(name)
        return type_name


class TypeSystem:
    """Handles type checking and conversions"""

    @staticmethod
    def check_binary_op(left: Any, right: Any, op: str) -> bool:
        """Check if binary operation is valid"""
        if op in ['+', '-', '*', '/']:
            # Arithmetic operations
            if op == '+':
                # Addition works for numbers and strings
                return (isinstance(left, (int, float)) and isinstance(right, (int, float))) or \
                       (isinstance(left, str) and isinstance(right, str))
            else:
                # Other arithmetic operations only work for numbers
                return isinstance(left, (int, float)) and isinstance(right, (int, float))
        elif op in ['==', '!=']:
            # Equality comparison works for same types
            return type(left) == type(right)
        elif op in ['<', '>', '<=', '>=']:
            # Ordering comparison works for numbers and strings
            return (isinstance(left, (int, float)) and isinstance(right, (int, float))) or \
                   (isinstance(left, str) and isinstance(right, str))
        elif op in ['&&', '||']:
            # Logical operations work for any types (truthy/falsy)
            return True
        return False

    @staticmethod
    def convert_to_type(value: Any, target_type: str) -> Any:
        """Convert value to target type"""
        if value is None:
            return None

        converters = {
            'int': int,
            'float': float,
            'string': str,
            'bool': bool
        }

        if target_type in converters:
            try:
                return converters[target_type](value)
            except (ValueError, TypeError) as e:
                raise TypeMismatchError(
                    f"Cannot convert {value} to {target_type}: {e}")

        raise TypeMismatchError(f"Unknown type: {target_type}")


class ReturnException(Exception):
    """Exception used for return statement control flow"""

    def __init__(self, value: Any):
        self.value = value





class Evaluator:
    """AST evaluator using visitor pattern"""

    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        # name -> (params, body, return_type)
        self.functions: Dict[str, tuple] = {}
        self.type_system = TypeSystem()
        self.builtins = BuiltinRegistry()

    def evaluate(self, node: ASTNode) -> Any:
        """Main evaluation method that dispatches to specific evaluators"""
        method_name = f'evaluate_{type(node).__name__}'
        method = getattr(self, method_name, None)
        if method is None:
            raise EvaluationError(f"No evaluator for {type(node).__name__}")
        return method(node)

    def _token_to_operator(self, token_type: TokenType) -> str:
        """Convert TokenType to string operator for evaluation"""
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
            # Fast operations are handled specially
            TokenType.FAST_INCREMENT: '+',
            TokenType.FAST_DECREMENT: '-',
            TokenType.FAST_ADD_ASSIGN: '+',
            TokenType.FAST_SUB_ASSIGN: '-',
        }
        return mapping.get(token_type, str(token_type))

    # AST Node Evaluators
    def evaluate_Program(self, node: Program) -> Any:
        """Evaluate a program (list of statements)"""
        result = None
        for statement in node.statements:
            result = self.evaluate(statement)
        return result

    def evaluate_Literal(self, node: Literal) -> Any:
        """Evaluate a literal value"""
        return node.value

    def evaluate_Variable(self, node: Variable) -> Any:
        """Evaluate a variable reference"""
        value, _ = self.current_scope.get(node.name)
        return value

    def evaluate_BinaryOp(self, node: BinaryOp) -> Any:
        """Evaluate a binary operation"""
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = self._token_to_operator(node.operator) if isinstance(node.operator, TokenType) else node.operator

        # Arithmetic operators
        if op in ('+', '-', '*', '/'):
            if op == '+':
                if not self.type_system.check_binary_op(left, right, op):
                    raise TypeMismatchError(
                        f"Type mismatch for '+': {type(left).__name__} and {type(right).__name__}")
                return left + right
            elif op == '-':
                if not self.type_system.check_binary_op(left, right, op):
                    raise TypeMismatchError(
                        f"Type mismatch for '-': {type(left).__name__} and {type(right).__name__}")
                return left - right
            elif op == '*':
                if not self.type_system.check_binary_op(left, right, op):
                    raise TypeMismatchError(
                        f"Type mismatch for '*': {type(left).__name__} and {type(right).__name__}")
                return left * right
            elif op == '/':
                if not self.type_system.check_binary_op(left, right, op):
                    raise TypeMismatchError(
                        f"Type mismatch for '/': {type(left).__name__} and {type(right).__name__}")
                if right == 0:
                    raise EvaluationError("division by zero")
                return left // right if isinstance(left, int) and isinstance(right, int) else float(left) / float(right)

        # Logical and comparison operators
        if op in ('||', '&&', '==', '!=', '<=', '>=', '<', '>'):
            operations = {
                '||': lambda l, r: l or r,
                '&&': lambda l, r: l and r,
                '==': lambda l, r: l == r,
                '!=': lambda l, r: l != r,
                '<=': lambda l, r: l <= r,
                '>=': lambda l, r: l >= r,
                '<': lambda l, r: l < r,
                '>': lambda l, r: l > r
            }
            return operations[op](left, right)

        raise EvaluationError(f"Unknown binary operator: {op}")  # Changed to show converted op

    def evaluate_UnaryOp(self, node: UnaryOp) -> Any:
        """Evaluate a unary operation"""
        operand = self.evaluate(node.operand)
        op = self._token_to_operator(node.operator) if isinstance(node.operator, TokenType) else node.operator

        if op == '!':
            return not operand
        elif op == '-':
            if not isinstance(operand, (int, float)):
                raise TypeMismatchError(
                    f"Unsupported operand type for unary '-': {type(operand).__name__}")
            return -operand

        raise EvaluationError(f"Unknown unary operator: {op}")

    def evaluate_FunctionCall(self, node: FunctionCall) -> Any:
        """Evaluate a function call"""
        func_name = node.name
        args = [self.evaluate(arg) for arg in node.args]

        # Check built-in functions first
        if self.builtins.has_function(func_name):
            return self.builtins.call(func_name, args)

        # Check user-defined functions
        if func_name in self.functions:
            func_params, func_body, func_ret_type = self.functions[func_name]
            if len(args) != len(func_params):
                raise EvaluationError(
                    f"{func_name}() expects {len(func_params)} args, got {len(args)}")

            # Create new scope for function execution
            return self.with_new_scope(lambda: self._execute_function(func_params, func_body, func_ret_type, args))()

        raise UndefinedFunctionError(f"Unknown function: {func_name}")

    def _token_to_type_string(self, token_type: TokenType) -> str:
        """Convert TokenType to type string"""
        mapping = {
            TokenType.INT_TYPE: 'int',
            TokenType.FLOAT_TYPE: 'float',
            TokenType.STRING_TYPE: 'string',
            TokenType.BOOL_TYPE: 'bool',
        }
        return mapping.get(token_type, str(token_type))

    def evaluate_Declaration(self, node: Declaration) -> Any:
        """Evaluate a variable declaration"""
        value = self.evaluate(node.initializer) if node.initializer else None
        
        type_name = self._token_to_type_string(node.type_name) if isinstance(node.type_name, TokenType) else node.type_name

        if value is not None:
            value = self.type_system.convert_to_type(value, type_name)

        self.current_scope.define(node.var_name, value, type_name)
        return value

    def evaluate_Assignment(self, node: Assignment) -> Any:
        """Evaluate a variable assignment"""
        value = self.evaluate(node.value)
        type_name = self.current_scope.get_type(node.var_name)
        value = self.type_system.convert_to_type(value, type_name)
        self.current_scope.set(node.var_name, value)
        return value

    def evaluate_IfStatement(self, node: IfStatement) -> Any:
        """Evaluate an if statement"""
        condition = self.evaluate(node.condition)
        if condition:
            return self.with_new_scope(lambda: self._execute_block(node.then_branch))()
        elif node.else_branch:
            return self.with_new_scope(lambda: self._execute_block(node.else_branch))()
        return None

    def evaluate_WhileStatement(self, node: WhileStatement) -> Any:
        """Evaluate a while statement"""
        result = None
        while self.evaluate(node.condition):
            result = self.with_new_scope(lambda: self._execute_block(node.body))()
        return result

    def evaluate_FunctionDeclaration(self, node: FunctionDeclaration) -> Any:
        """Evaluate a function declaration"""
        self.functions[node.name] = (node.params, node.body, node.return_type)
        return f"<function {node.name}>"

    def evaluate_ReturnStatement(self, node: ReturnStatement) -> Any:
        """Evaluate a return statement"""
        value = self.evaluate(node.value) if node.value else None
        raise ReturnException(value)

    def evaluate_ExpressionStatement(self, node: ExpressionStatement) -> Any:
        """Evaluate an expression statement"""
        return self.evaluate(node.expression)

    def _execute_function(self, params, body, return_type, args):
        """Execute a function with given parameters and arguments"""
        # Bind parameters to arguments
        for param, arg_val in zip(params, args):
            param_type, param_name = param
            param_type_str = self._token_to_type_string(param_type) if isinstance(param_type, TokenType) else param_type
            converted_arg = self.type_system.convert_to_type(
                arg_val, param_type_str)
            self.current_scope.define(param_name, converted_arg, param_type_str)

        try:
            result = self._execute_block(body)
            if return_type:
                return_type_str = self._token_to_type_string(return_type) if isinstance(return_type, TokenType) else return_type
                result = self.type_system.convert_to_type(result, return_type_str)
            return result
        except ReturnException as ret:
            if return_type:
                return_type_str = self._token_to_type_string(return_type) if isinstance(return_type, TokenType) else return_type
                return self.type_system.convert_to_type(ret.value, return_type_str)
            return ret.value

    def _execute_block(self, statements):
        """Execute a block of statements"""
        result = None
        for stmt in statements:
            result = self.evaluate(stmt)
        return result

    def with_new_scope(self, func):
        """Context manager for creating new scopes"""
        def wrapper(*args, **kwargs):
            old_scope = self.current_scope
            self.current_scope = Scope(parent=old_scope)
            try:
                return func(*args, **kwargs)
            finally:
                self.current_scope = old_scope
        return wrapper
