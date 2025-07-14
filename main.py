import sys

import Lexer
import Parser
import Evaluator


def run(code, env):
    tokens = Lexer.tokenize(code)
    print(tokens)
    parser = Parser.Parser(tokens)
    ast = parser.parse()
    print(ast)
    result = env.evaluate(ast)
    print(result)
    return result

def console_mode():
    env = Evaluator.Environment()
    while True:
        code = input("> ")
        if code.strip().lower() == 'exit':
            break
        if code.strip():
            run(code, env)

def file_mode():
    env = Evaluator.Environment()
    filepath = sys.argv[1]
    try:
        with open(filepath, 'r') as file:
            code = file.read()
        for line in code.splitlines():
            if line.strip():
                try:
                    run(line, env)
                except Exception as e:
                    print(f"Error on line: {line}\n{e}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_mode()
    else:
        console_mode()
