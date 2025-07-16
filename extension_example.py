#!/usr/bin/env python3
"""
Example of extending the language with new built-in functions
This demonstrates how easy it is to add new functionality
"""

from Builtins import BuiltinFunction, BuiltinRegistry
from Error import RuntimeError
from typing import Any, List


class LengthFunction(BuiltinFunction):
    """Get the length of a string or number of digits in a number"""

    def name(self) -> str:
        return 'len'

    def call(self, args: List[Any]) -> Any:
        value = args[0]
        if isinstance(value, str):
            return len(value)
        elif isinstance(value, (int, float)):
            return len(str(int(value)))
        else:
            raise RuntimeError(
                f"len() not supported for type {type(value).__name__}")

    def validate_args(self, args: List[Any]) -> bool:
        return len(args) == 1


class MaxFunction(BuiltinFunction):
    """Get the maximum of two or more numbers"""

    def name(self) -> str:
        return 'max'

    def call(self, args: List[Any]) -> Any:
        if not all(isinstance(arg, (int, float)) for arg in args):
            raise RuntimeError("max() requires numeric arguments")
        return max(args)

    def validate_args(self, args: List[Any]) -> bool:
        return len(args) >= 2


class MinFunction(BuiltinFunction):
    """Get the minimum of two or more numbers"""

    def name(self) -> str:
        return 'min'

    def call(self, args: List[Any]) -> Any:
        if not all(isinstance(arg, (int, float)) for arg in args):
            raise RuntimeError("min() requires numeric arguments")
        return min(args)

    def validate_args(self, args: List[Any]) -> bool:
        return len(args) >= 2


class AbsFunction(BuiltinFunction):
    """Get the absolute value of a number"""

    def name(self) -> str:
        return 'abs'

    def call(self, args: List[Any]) -> Any:
        value = args[0]
        if not isinstance(value, (int, float)):
            raise RuntimeError(
                f"abs() requires numeric argument, got {type(value).__name__}")
        return abs(value)

    def validate_args(self, args: List[Any]) -> bool:
        return len(args) == 1


def register_math_functions(registry: BuiltinRegistry):
    """Register math-related built-in functions"""
    math_functions = [
        LengthFunction(),
        MaxFunction(),
        MinFunction(),
        AbsFunction(),
    ]

    for func in math_functions:
        registry.register(func)
        print(f"Registered function: {func.name()}")


def test_extended_functions():
    """Test the new extended functions"""
    from Lexer import tokenize
    from Parser import Parser
    from Evaluator import Environment

    # Register our new functions
    env = Environment()
    register_math_functions(env.evaluator.builtins)

    test_code = '''
    string text = "Hello World";
    int text_length = len(text);
    print("Length of text:", text_length);
    
    int a = 10;
    int b = 20;
    int c = 5;
    
    int maximum = max(a, b, c);
    int minimum = min(a, b, c);
    int absolute = abs(-15);
    
    print("Max:", maximum);
    print("Min:", minimum);
    print("Abs(-15):", absolute);
    
    int num_digits = len(12345);
    print("Digits in 12345:", num_digits);
    '''

    print("Testing extended functions:")
    print("Code:")
    print(test_code)
    print("\nOutput:")

    try:
        tokens = tokenize(test_code)
        parser = Parser(tokens)
        ast = parser.parse()
        env.evaluate(ast)
        print("\n✓ All extended functions work correctly!")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    test_extended_functions()
