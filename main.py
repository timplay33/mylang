import sys

import Lexer
import Parser
import Evaluator



def run(code, env):
    tokens = []
    ast = []
    try:
        tokens = Lexer.tokenize(code)
        parser = Parser.Parser(tokens)
        ast = parser.parse()
        env.evaluate(ast)
    except Exception as e:
        print('\x1b[0;30;41m' + f" {type(e).__name__}: {e} " + '\x1b[0m')
        if tokens:
            print('\033[91m'+ f"Tokens: {"[\n" + ",\n".join(f"    {repr(t)}" for t in tokens) + "\n]"}" +'\033[0m')
        if ast:
            print('\033[91m'+ f"AST: {"[\n" + ",\n".join(f"    {repr(a)}" for a in ast) + "\n]"}"+ '\033[0m')
        sys.exit(1)

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
            run(code, env)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_mode()
    else:
        console_mode()
