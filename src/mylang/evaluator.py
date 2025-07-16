from typing import Any, Dict, List, Optional, Union
from .ast import *
from .error import *
from .builtins import BuiltinRegistry


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


class Environment:
    """Legacy environment class for backward compatibility"""

    def __init__(self):
        self.evaluator = Evaluator()

    @property
    def vars(self):
        """Legacy vars property"""
        return {name: (value, type_name) for name, (value, type_name) in self.evaluator.current_scope.variables.items()}

    @property
    def funcs(self):
        """Legacy funcs property"""
        return self.evaluator.functions

    def evaluate(self, node):
        """Legacy evaluate method"""
        return self.evaluator.evaluate_legacy(node)

    def formatVar(self, type_name, value):
        """Legacy formatVar method"""
        return self.evaluator.type_system.convert_to_type(value, type_name)


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

    def evaluate_legacy(self, node) -> Any:
        """Evaluate legacy tuple-based AST nodes for backward compatibility"""
        if isinstance(node, list):
            result = None
            for statement in node:
                result = self.evaluate_legacy(statement)
            return result

        if isinstance(node, (int, float, str, bool, type(None))):
            return node

        if isinstance(node, tuple):
            op = node[0]

            # Arithmetic operators
            if op in ('+', '-', '*', '/'):
                left = self.evaluate_legacy(node[1])
                right = self.evaluate_legacy(
                    node[2]) if len(node) > 2 else None

                if op == '+':
                    if not self.type_system.check_binary_op(left, right, op):
                        raise TypeMismatchError(
                            f"Type mismatch for '+': {type(left).__name__} and {type(right).__name__}")
                    return left + right
                elif op == '-':
                    if right is not None:
                        if not self.type_system.check_binary_op(left, right, op):
                            raise TypeMismatchError(
                                f"Type mismatch for '-': {type(left).__name__} and {type(right).__name__}")
                        return left - right
                    else:
                        if not isinstance(left, (int, float)):
                            raise TypeMismatchError(
                                f"Unsupported operand type for unary '-': {type(left).__name__}")
                        return -left
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
                left = self.evaluate_legacy(node[1])
                right = self.evaluate_legacy(node[2])

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

            if op == '!':
                return not self.evaluate_legacy(node[1])

            if op == 'expr_stmt':
                return self.evaluate_legacy(node[1])

            if op == 'decl':
                _, type_str, name, expr = node
                value = self.evaluate_legacy(expr) if expr else None

                if value is not None:
                    value = self.type_system.convert_to_type(value, type_str)

                self.current_scope.define(name, value, type_str)
                return value

            if op == 'assign':
                name = node[1]
                value = self.evaluate_legacy(node[2])
                type_name = self.current_scope.get_type(name)
                value = self.type_system.convert_to_type(value, type_name)
                self.current_scope.set(name, value)
                return value

            if op == 'var':
                name = node[1]
                value, _ = self.current_scope.get(name)
                return value

            if op == 'call':
                func_name = node[1]
                args = [self.evaluate_legacy(arg) for arg in node[2]]

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

            if op == 'func':
                name = node[1]
                params = node[2]
                body = node[3]
                return_type = node[4] if len(node) > 4 else None
                self.functions[name] = (params, body, return_type)
                return f"<function {name}>"

            if op == 'return':
                value = self.evaluate_legacy(
                    node[1]) if len(node) > 1 else None
                raise ReturnException(value)

            if op == 'if':
                condition = self.evaluate_legacy(node[1])
                if condition:
                    return self.with_new_scope(lambda: self._execute_block(node[2]))()
                elif len(node) > 3:  # else clause
                    return self.with_new_scope(lambda: self._execute_block(node[3]))()
                return None

            if op == 'while':
                condition = node[1]
                body = node[2]
                result = None
                while self.evaluate_legacy(condition):
                    result = self.with_new_scope(
                        lambda: self._execute_block(body))()
                return result

        raise EvaluationError(f"Invalid AST node: {node}")

    def _execute_function(self, params, body, return_type, args):
        """Execute a function with given parameters and arguments"""
        # Bind parameters to arguments
        for param, arg_val in zip(params, args):
            param_type, param_name = param
            converted_arg = self.type_system.convert_to_type(
                arg_val, param_type)
            self.current_scope.define(param_name, converted_arg, param_type)

        try:
            result = self._execute_block(body)
            if return_type:
                result = self.type_system.convert_to_type(result, return_type)
            return result
        except ReturnException as ret:
            if return_type:
                return self.type_system.convert_to_type(ret.value, return_type)
            return ret.value

    def _execute_block(self, statements):
        """Execute a block of statements"""
        result = None
        for stmt in statements:
            result = self.evaluate_legacy(stmt)
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
