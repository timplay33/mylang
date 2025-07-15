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
        print('\033[101m\33[30m' + f" {type(e).__name__}: {e} " + '\033[0m')
        if tokens:
            print('\033[91m'+ f"Tokens: {"[\n" + ",\n".join(f"{i}:    {repr(t)}" for i, t in enumerate(tokens)) + "\n]"}" +'\033[0m')
        if ast:
            print('\033[91m'+ f"AST: {"[\n" + ",\n".join(f"    {repr(a)}" for a in ast) + "\n]"}"+ '\033[0m')
        if len(env.vars) > 0: print('\033[93m'+ f"Global Variables: {env.vars}" + '\033[0m')
        if len(env.funcs) > 0:print('\033[93m'+ f"Global Functions: {env.funcs}" + '\033[0m')
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
