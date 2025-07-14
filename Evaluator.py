class Environment:

    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def evaluate(self, node):
        if isinstance(node, (int, float, str)):
            return node
        if isinstance(node, tuple):
            op = node[0]
            if op == '+': return self.evaluate(node[1]) + self.evaluate(node[2])
            elif op == '-': return self.evaluate(node[1]) - self.evaluate(node[2])
            elif op == '*': return self.evaluate(node[1]) * self.evaluate(node[2])
            elif op == '/': return self.evaluate(node[1]) / self.evaluate(node[2])
            elif op == 'neg': return -self.evaluate(node[1])
            elif op == 'assign': 
                name = node[1]
                value = self.evaluate(node[2])
                self.vars[name] = value
                return value
            elif op == 'var': 	
                name = node[1]
                if name not in self.vars:
                    raise NameError(f"Undefined variable: {name}")
                return self.vars[name]
            elif op == 'call':
                func_name = node[1]
                args = [self.evaluate(arg) for arg in node[2]]
                if func_name == 'print':
                    print(*args)
                    return None
                elif func_name in self.funcs:
                    func_params, func_body = self.funcs[func_name]
                    if len(args) != len(func_params):
                        raise TypeError(f"{func_name}() expects {len(func_params)} args, got {len(args)}")
                    
                    local = Environment()
                    local.funcs = self.funcs
                    local.vars = self.vars.copy()
                    for param, arg_val in zip(func_params, args):
                        local.vars[param] = arg_val
                    print(local.vars, local.funcs)
                    return local.evaluate(func_body)
                else:
                    raise NameError(f"Unknown function: {func_name}")
            elif op == 'func':
                name = node[1]
                params = node[2]
                body = node[3]
                self.funcs[name] = (params, body)
                return f"<function {name}>"

        raise TypeError(f"Invalid AST node: {node}")
