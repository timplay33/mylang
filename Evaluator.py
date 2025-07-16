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
            op = node[0]
            # Arithmetic operators
            if op in ('+', '-', '*', '/'):
                left = self.evaluate(node[1])
                right = self.evaluate(node[2]) if len(node) > 2 else None
                if op == '+':
                    if type(left) != type(right):
                        raise TypeError(
                            f"Type mismatch for '+': {type(left).__name__} and {type(right).__name__}")
                    return left + right
                elif op == '-':
                    if right is not None:
                        if type(left) != type(right):
                            raise TypeError(
                                f"Type mismatch for '-': {type(left).__name__} and {type(right).__name__}")
                        if not isinstance(left, (int, float)):
                            raise TypeError(
                                f"Unsupported operand type for '-': {type(left).__name__}")
                        return left - right
                    else:
                        if not isinstance(left, (int, float)):
                            raise TypeError(
                                f"Unsupported operand type for unary '-': {type(left).__name__}")
                        return -left
                elif op == '*':
                    if type(left) != type(right):
                        raise TypeError(
                            f"Type mismatch for '*': {type(left).__name__} and {type(right).__name__}")
                    if not isinstance(left, (int, float)):
                        raise TypeError(
                            f"Unsupported operand type for '*': {type(left).__name__}")
                    return left * right
                elif op == '/':
                    if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                        raise TypeError(
                            f"Unsupported operand type for '/': {type(left).__name__} and {type(right).__name__}")
                    if right == 0:
                        raise ZeroDivisionError("division by zero")
                    return left // right if isinstance(left, int) and isinstance(right, int) else float(left) / float(right)

            # Logical and comparison operators
            if op in ('||', '&&', '==', '!=', '<=', '>=', '<', '>'):
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                return {
                    '||': left or right,
                    '&&': left and right,
                    '==': left == right,
                    '!=': left != right,
                    '<=': left <= right,
                    '>=': left >= right,
                    '<': left < right,
                    '>': left > right
                }[op]

            if op == '!':
                return not self.evaluate(node[1])

            if op in ('++', '--'):
                inc = node[2] if len(node) > 2 else 1
                val, typ = self.vars[node[1]]
                self.vars[node[1]] = (
                    val + inc if op == '++' else val - inc, typ)
                return None

            if op == 'expr_stmt':
                return self.evaluate(node[1])

            if op == 'decl':
                _, type_str, name, expr = node
                value = self.evaluate(expr)
                if name in self.vars:
                    raise NameError(f"Variable '{name}' already declared")
                if type_str == 'int' and not isinstance(value, (int, type(None))):
                    raise RuntimeError(
                        f"Expected int, got {type(value).__name__}")
                if type_str == 'float' and not isinstance(value, (float, int, type(None))):
                    raise RuntimeError(
                        f"Expected float, got {type(value).__name__}")
                if type_str == 'string' and not isinstance(value, (str, type(None))):
                    raise RuntimeError(
                        f"Expected string, got {type(value).__name__}")
                if type_str == 'bool' and not isinstance(value, (bool, type(None))):
                    raise RuntimeError(
                        f"Expected bool, got {type(value).__name__}")
                self.vars[name] = (value, type_str)
                return value

            if op == 'assign':
                name = node[1]
                if name not in self.vars:
                    raise NameError(f"Undefined variable: {name}")
                value = self.formatVar(
                    self.vars[name][1], self.evaluate(node[2]))
                self.vars[name] = (value, self.vars[name][1])
                return value

            if op == 'var':
                name = node[1]
                if name not in self.vars:
                    raise NameError(f"Undefined variable: {name}")
                return self.formatVar(self.vars[name][1], self.vars[name][0])

            if op == 'call':
                func_name = node[1]
                args = [self.evaluate(arg) for arg in node[2]]
                if func_name == 'print':
                    print(*args)
                    return None
                if func_name == 'toInt':
                    return int(args[0])
                if func_name == 'toString':
                    return str(args[0])
                if func_name == 'toFloat':
                    return float(args[0])
                if func_name in self.funcs:
                    func_params, func_body, func_ret_type = self.funcs[func_name]
                    if len(args) != len(func_params):
                        raise TypeError(
                            f"{func_name}() expects {len(func_params)} args, got {len(args)}")
                    local = Environment()
                    local.funcs = self.funcs
                    local.vars = self.vars.copy()
                    for param, arg_val in zip(func_params, args):
                        local.vars[param[1]] = (arg_val, param[0])
                    result = local.evaluate(func_body)
                    if func_ret_type:
                        result = self.formatVar(func_ret_type, result)
                    return result
                raise NameError(f"Unknown function: {func_name}")

            if op == 'func':
                name = node[1]
                params = node[2]
                body = node[3]
                return_type = node[4] if len(node) > 4 else None
                self.funcs[name] = (params, body, return_type)
                return f"<function {name}>"

            if op == 'return':
                return self.evaluate(node[1])

            if op == 'if':
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

            if op == 'while':
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
        converters = {
            'int': int,
            'float': float,
            'string': str,
            'bool': bool
        }
        if value is None:
            return None
        if type in converters:
            return converters[type](value)
        raise TypeError(f"Unknown type: {type}")
