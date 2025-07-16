#!/usr/bin/env python3
"""
Test the refactored language system
"""
from Lexer import tokenize
from Parser import Parser
from Evaluator import Environment


def test_basic_functionality():
    """Test basic functionality with the new system"""
    code = '''
    int x = 10;
    int y = 20;
    int result = x + y;
    print(result);
    '''

    print("Testing basic functionality...")
    print(f"Code: {code}")

    # Tokenize
    tokens = tokenize(code)
    print(f"Tokens: {tokens[:10]}...")  # Show first 10 tokens

    # Parse
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}")

    # Evaluate
    env = Environment()
    result = env.evaluate(ast)
    print(f"Result: {result}")
    print("Variables:", env.vars)


def test_function_definition():
    """Test function definition and calling"""
    code = '''
    func int add(int a, int b) {
        return a + b;
    }
    
    int result = add(5, 3);
    print(result);
    '''

    print("\nTesting function definition...")
    print(f"Code: {code}")

    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        env = Environment()
        result = env.evaluate(ast)
        print(f"Result: {result}")
        print("Functions:", env.funcs)
    except Exception as e:
        print(f"Error: {e}")


def test_error_handling():
    """Test improved error handling"""
    code = '''
    int x = "hello";  // Type mismatch
    '''

    print("\nTesting error handling...")
    print(f"Code: {code}")

    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        env = Environment()
        result = env.evaluate(ast)
    except Exception as e:
        print(f"Caught error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    test_basic_functionality()
    test_function_definition()
    test_error_handling()
