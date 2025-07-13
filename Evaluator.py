def evaluate(node):
    if isinstance(node, float):
        return node
    op, left, right = node
    if op == '+': return evaluate(left) + evaluate(right)
    if op == '-': return evaluate(left) - evaluate(right)
    if op == '*': return evaluate(left) * evaluate(right)
    if op == '/': return evaluate(left) / evaluate(right)
    return None
