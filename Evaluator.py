class Environment:

    def __init__(self):
        self.vars = {}

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
                else:
                    raise NameError(f"Unknown function: {func_name}")
        raise TypeError(f"Invalid AST node: {node}")
