class Environment:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def evaluate(self, node):
        if isinstance(node, list):  # Add support for lists of statements
            result = None
            for statement in node:
                result = self.evaluate(statement)
            return result
            
        if isinstance(node, (int, float, str)):
            return node
        if isinstance(node, tuple):
            match node[0]:
                case '+': return self.evaluate(node[1]) + self.evaluate(node[2])
                case '-': return self.evaluate(node[1]) - self.evaluate(node[2])
                case '*': return self.evaluate(node[1]) * self.evaluate(node[2])
                case '/': return self.evaluate(node[1]) / self.evaluate(node[2])
                case 'neg': return -self.evaluate(node[1])
                case 'assign': 
                    name = node[1]
                    value = self.evaluate(node[2])
                    self.vars[name] = value
                    return value
                case 'var': 	
                    name = node[1]
                    if name not in self.vars:
                        raise NameError(f"Undefined variable: {name}")
                    return self.vars[name]
                case 'call':
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
                        return local.evaluate(func_body)
                    else:
                        raise NameError(f"Unknown function: {func_name}")
                case 'func':
                    name = node[1]
                    params = node[2]
                    body = node[3]
                    self.funcs[name] = (params, body)
                    return f"<function {name}>"

                case 'return':
                    value = self.evaluate(node[1])
                    return value
                case 'if':
                    condition = self.evaluate(node[1])
                    if condition:
                        result = None
                        local_env = Environment()
                        local_env.vars = self.vars
                        for stmt in node[2]:
                            result = local_env.evaluate(stmt)
                        return result
                    elif len(node) > 3:  # Check for else clause
                        result = None
                        local_env = Environment()
                        local_env.vars = self.vars
                        for stmt in node[3]:
                            result = local_env.evaluate(stmt)
                        return result
                    return None
                case 'while':
                    condition = node[1]
                    body = node[2]
                    while self.evaluate(condition):
                        local_env = Environment()
                        local_env.vars = self.vars
                        for stmt in body:
                            local_env.evaluate(stmt)
                    return None

        raise TypeError(f"Invalid AST node: {node}")