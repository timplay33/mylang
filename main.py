#!/usr/bin/env python3
"""
MyLang Interpreter - Main Entry Point
Usage: python main.py [file.mylang]
       python -m mylang [file.mylang]
"""

import sys
import os

# Add src to path so we can import mylang
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mylang import tokenize, Parser, Evaluator, LanguageError

def run(code, env, filename=None):
    """Execute MyLang code with improved error handling"""
    tokens = []
    ast = []

    try:
        # Tokenize
        tokens = tokenize(code)

        # Parse
        parser = Parser(tokens)
        ast = parser.parse()

        # Evaluate
        result = env.evaluate(ast)
        return result

    except LanguageError as e:
        # Our custom language errors with better formatting
        print(f'\033[101m\033[30m {type(e).__name__}: {e} \033[0m')
        _print_debug_info(tokens, ast, env, filename)
        sys.exit(1)

    except Exception as e:
        # Unexpected errors
        print(f'\033[101m\033[30m Unexpected {type(e).__name__}: {e} \033[0m')
        _print_debug_info(tokens, ast, env, filename)
        sys.exit(1)


def _print_debug_info(tokens, ast, env, filename=None):
    """Print debug information when errors occur"""
    if filename:
        print(f'\033[93mFile: {filename}\033[0m')

    if tokens:
        print('\033[91mTokens:\033[0m')
        for i, token in enumerate(tokens[:20]):  # Show first 20 tokens
            print(f"  {i}: {repr(token)}")
        if len(tokens) > 20:
            print(f"  ... and {len(tokens) - 20} more tokens")

    if ast:
        print('\033[91mAST:\033[0m')
        # Handle Program AST node
        for i, node in enumerate(ast.statements[:10]):  # Show first 10 AST nodes
            print(f"  {i}: {repr(node)}")
        if len(ast.statements) > 10:
            print(f"  ... and {len(ast.statements) - 10} more nodes")

    if env.global_scope.variables:
        vars_dict = {name: (value, type_name) for name, (value, type_name) in env.global_scope.variables.items()}
        print(f'\033[93mGlobal Variables: {vars_dict}\033[0m')

    if env.functions:
        print(f'\033[93mGlobal Functions: {list(env.functions.keys())}\033[0m')


def console_mode():
    """Interactive console mode for testing"""
    print("MyLang Interactive Console v1.0.0")
    print("Type 'exit' to quit")
    print("=" * 40)

    env = Evaluator()

    while True:
        try:
            code = input("> ")
            if code.strip().lower() == 'exit':
                break
            if code.strip():
                run(code, env)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


def file_mode():
    """Execute a MyLang file"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.mylang>")
        print("   or: python main.py --help")
        sys.exit(1)

    filepath = sys.argv[1]

    if filepath in ['--help', '-h']:
        show_help()
        return

    # Check if file exists
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    # Check file extension
    if not filepath.endswith('.mylang'):
        print("Warning: File doesn't have .mylang extension")

    env = Evaluator()

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            code = file.read()
            print(f"Executing {filepath}...")
            print("=" * 40)
            run(code, env, filepath)
            print("=" * 40)
            print("Execution completed successfully!")

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Cannot read file {filepath} - encoding issue")
        sys.exit(1)


def show_help():
    """Show help information"""
    print("MyLang Programming Language Interpreter v1.0.0")
    print()
    print("Usage:")
    print("  python main.py [file.mylang]    # Run a MyLang program")
    print("  python main.py                  # Start interactive console")
    print("  python main.py --help          # Show this help")
    print()
    print("Examples:")
    print("  python main.py examples/comprehensive_test.mylang")
    print("  python main.py")
    print()
    print("For more information, see README.md")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        file_mode()
    else:
        console_mode()


if __name__ == '__main__':
    main()
