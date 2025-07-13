import sys

import Lexer
import Parser
import Evaluator


def run(code):
    tokens = Lexer.tokenize(code)
    parser = Parser.Parser(tokens)
    ast = parser.parse()
    return Evaluator.evaluate(ast)

def console_mode():
    while True:
        code = input("> ")
        if code.strip().lower() == 'exit':
            break
        if code.strip():
            print(run(code))

def file_mode():
    filepath = sys.argv[1]
    try:
        with open(filepath, 'r') as file:
            code = file.read()
        if not code.strip():
            print("File is empty.")
            sys.exit(1)
        print(run(code))
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_mode()
    else:
        console_mode()