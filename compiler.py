import re

TOKEN_SPEC = [
    ("NUMBER",   r'\d+'),
    ("ASSIGN",   r'='),
    ("SET",      r'set'),
    ("IF",       r'if'),
    ("PRINT",    r'print'),
    ("ID",       r'[A-Za-z_]\w*'),
    ("OP",       r'[+\-*/><]=?|=='),
    ("NEWLINE",  r'\n'),
    ("SKIP",     r'[ \t]+'),
]

token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC))

def tokenize(code):
    tokens = []
    for match in token_re.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind == "NUMBER":
            value = int(value)
        if kind not in ("SKIP", "NEWLINE"):
            tokens.append((kind, value))
    return tokens

class MiniLang:
    def __init__(self):
        self.vars = {}

    def execute(self, tokens):
        i = 0
        while i < len(tokens):
            tok_type, tok_val = tokens[i]

            if tok_type == "SET":
                var_name = tokens[i+1][1]
                value = tokens[i+3][1]
                self.vars[var_name] = value
                i += 4

            elif tok_type == "ID" and tokens[i+1][0] == "ASSIGN":
                var_name = tok_val
                expr_val = self.eval_expr(tokens[i+2:i+5])
                self.vars[var_name] = expr_val
                i += 5

            elif tok_type == "IF":
                left = tokens[i+1][1]
                op = tokens[i+2][1]
                right = tokens[i+3][1]
                condition = self.compare(left, op, right)
                i += 4
                if condition and tokens[i][0] == "PRINT":
                    print_val = tokens[i+1][1]
                    print(self.vars.get(print_val, print_val))
                    i += 2

            elif tok_type == "PRINT":
                var_name = tokens[i+1][1]
                print(self.vars.get(var_name, var_name))
                i += 2
            else:
                i += 1

    def eval_expr(self, expr_tokens):
        left = expr_tokens[0][1]
        if isinstance(left, str):
            left = self.vars.get(left, 0)
        op = expr_tokens[1][1]
        right = expr_tokens[2][1]
        if isinstance(right, str):
            right = self.vars.get(right, 0)

        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': return left / right
        return 0

    def compare(self, left, op, right):
        if isinstance(left, str):
            left = self.vars.get(left, 0)
        if isinstance(right, str):
            right = self.vars.get(right, 0)
        if op == '>': return left > right
        if op == '<': return left < right
        if op == '==': return left == right
        if op == '>=': return left >= right
        if op == '<=': return left <= right
        return False


if __name__ == "__main__":
    with open("program.mini", "r") as f:
        code = f.read()
    tokens = tokenize(code)
    interpreter = MiniLang()
    interpreter.execute(tokens)
