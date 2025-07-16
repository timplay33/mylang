#!/usr/bin/env python3
"""
Demonstration of the improved language features
"""
from Lexer import tokenize
from Parser import Parser
from Evaluator import Environment, Evaluator
from AST import *
from Error import *
from Builtins import BuiltinRegistry


def demo_improved_error_handling():
    """Demonstrate improved error handling with source locations"""
    print("=== Improved Error Handling Demo ===")

    test_cases = [
        ("Type mismatch", 'int x = "hello";'),
        ("Undefined variable", 'print(undefinedVar);'),
        ("Undefined function", 'unknownFunc();'),
        ("Wrong argument count", 'toInt(1, 2);'),
    ]

    for desc, code in test_cases:
        print(f"\n{desc}:")
        print(f"Code: {code}")
        try:
            tokens = tokenize(code)
            parser = Parser(tokens)
            ast = parser.parse()
            env = Environment()
            env.evaluate(ast)
        except Exception as e:
            print(f"✓ Caught {type(e).__name__}: {e}")


def demo_scope_system():
    """Demonstrate proper scoping"""
    print("\n=== Scope System Demo ===")

    code = '''
    int global_var = 100;
    
    func int test_scope(int param) {
        int local_var = param * 2;
        return local_var + global_var;
    }
    
    int result = test_scope(5);
    print("Result:", result);
    '''

    print(f"Code:\n{code}")

    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        env = Environment()
        env.evaluate(ast)
        print("✓ Scoping works correctly!")
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_builtin_system():
    """Demonstrate extensible builtin system"""
    print("\n=== Builtin System Demo ===")

    # Get the builtin registry
    evaluator = Evaluator()
    builtins = evaluator.builtins

    print("Available builtin functions:")
    for name in builtins.functions:
        print(f"  - {name}")

    # Test type conversions
    code = '''
    int x = toInt("42");
    float y = toFloat(x);
    string z = toString(y);
    print("Converted:", z);
    '''

    print(f"\nTesting type conversions:\n{code}")

    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        env = Environment()
        env.evaluate(ast)
        print("✓ Type conversions work!")
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_type_system():
    """Demonstrate improved type checking"""
    print("\n=== Type System Demo ===")

    test_cases = [
        ("Valid string concatenation", 'string msg = "Hello " + "World"; print(msg);'),
        ("Valid number arithmetic", 'int result = 10 + 5 * 2; print(result);'),
        ("Type conversion", 'float f = toFloat(42); print(f);'),
    ]

    for desc, code in test_cases:
        print(f"\n{desc}:")
        print(f"Code: {code}")
        try:
            tokens = tokenize(code)
            parser = Parser(tokens)
            ast = parser.parse()
            env = Environment()
            env.evaluate(ast)
            print("✓ Success!")
        except Exception as e:
            print(f"✗ Error: {e}")


def demo_comprehensive_example():
    """Comprehensive example showing all improvements"""
    print("\n=== Comprehensive Example ===")

    code = '''
    // Function to calculate factorial
    func int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    
    // Test the function
    int num = 5;
    int result = factorial(num);
    print("Factorial of", num, "is", result);
    
    // Test type conversions
    string result_str = toString(result);
    print("As string:", result_str);
    '''

    print(f"Code:\n{code}")

    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        env = Environment()
        env.evaluate(ast)
        print("✓ Comprehensive example works!")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    demo_improved_error_handling()
    demo_scope_system()
    demo_builtin_system()
    demo_type_system()
    demo_comprehensive_example()
