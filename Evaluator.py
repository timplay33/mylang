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
            
        if isinstance(node, (int, float, str, bool, type(None))):
            return node
        if isinstance(node, tuple):
            match node[0]:
                case '+': return self.evaluate(node[1]) + self.evaluate(node[2])
                case '-': 
                    if (len(node) > 2):
                        return self.evaluate(node[1]) - self.evaluate(node[2])
                    elif (len(node) == 2):
                        return -self.evaluate(node[1])
                case '*': return self.evaluate(node[1]) * self.evaluate(node[2])
                case '/': return self.evaluate(node[1]) / self.evaluate(node[2])
                case '||': return self.evaluate(node[1]) or self.evaluate(node[2])
                case '&&': return self.evaluate(node[1]) and self.evaluate(node[2])
                case '==': return self.evaluate(node[1]) == self.evaluate(node[2])
                case '!=': return self.evaluate(node[1]) != self.evaluate(node[2])
                case '<=': return self.evaluate(node[1]) <= self.evaluate(node[2])
                case '>=': return self.evaluate(node[1]) >= self.evaluate(node[2])
                case '<': return self.evaluate(node[1]) < self.evaluate(node[2])
                case '>': return self.evaluate(node[1]) > self.evaluate(node[2])
                case '!': return not self.evaluate(node[1])
                case 'expr_stmt':
                    return self.evaluate(node[1])
                case 'decl':
                    _, type_str, name, expr = node
                    value = self.evaluate(expr)
                    if name in self.vars:
                        raise NameError(f"Variable '{name}' already declared")
                    if type_str == 'int' and not isinstance(value, (int, type(None))):
                        raise RuntimeError(f"Expected int, got {type(value).__name__}")
                    if type_str == 'float' and not isinstance(value, (float, int, type(None))):
                        raise RuntimeError(f"Expected float, got {type(value).__name__}")
                    if type_str == 'string' and not isinstance(value, (str, type(None))):
                        raise RuntimeError(f"Expected string, got {type(value).__name__}")
                    if type_str == 'bool' and not isinstance(value, (bool, type(None))):
                        raise RuntimeError(f"Expected bool, got {type(value).__name__}")
                    self.vars[name] = (value, type_str)
                    return value
                case 'assign': 
                    name = node[1]
                    if name not in self.vars:
                        raise NameError(f"Undefined variable: {name}")
                    value = self.formatVar(self.vars[name][1], self.evaluate(node[2]))
                    self.vars[name] = (value, self.vars[name][1])
                    return value
                case 'var': 	
                    name = node[1]
                    if name not in self.vars:
                        raise NameError(f"Undefined variable: {name}")
                    return self.formatVar(self.vars[name][1],self.vars[name][0])
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
                            local.vars[param[1]] = (arg_val, param[0])
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

    def formatVar(self, type, value):
        if type == 'int':
            return int(value) if value is not None else None
        elif type == 'float':
            return float(value) if value is not None else None
        elif type == 'string':
            return str(value) if value is not None else None
        elif type == 'bool':
            return bool(value) if value is not None else None
        else:
            raise TypeError(f"Unknown type: {type}")