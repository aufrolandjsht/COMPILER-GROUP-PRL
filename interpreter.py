from parser import (
    Program, Assign, Identifier, Number,
    BinaryOp, PrintStmt, IfStmt
)
from lexer import TokenType


class MiniLang:
    def __init__(self):
        self.vars = {}

    def execute(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.execute(stmt)

        elif isinstance(node, Assign):
            value = self.eval_expr(node.expr)
            self.vars[node.name] = value

        elif isinstance(node, PrintStmt):
            value = self.eval_expr(node.expr)
            print(value)

        elif isinstance(node, IfStmt):
            condition = self.eval_expr(node.condition)
            if condition:
                for stmt in node.body:
                    self.execute(stmt)
            else:
                handled = False
                # Handle ELSE IF blocks
                for cond, body in node.elif_blocks:
                    if self.eval_expr(cond):
                        for stmt in body:
                            self.execute(stmt)
                        handled = True
                        break
                # Handle ELSE
                if not handled and node.else_body:
                    for stmt in node.else_body:
                        self.execute(stmt)
        else:
            raise Exception(f"Unknown AST node: {node}")

    def eval_expr(self, node):
        if isinstance(node, Number):
            return node.value

        if isinstance(node, Identifier):
            return self.vars.get(node.name, 0)

        if isinstance(node, BinaryOp):
            left = self.eval_expr(node.left)
            right = self.eval_expr(node.right)
            return self.apply_op(left, node.op, right)

        return None

    def apply_op(self, left, op, right):
        if op == TokenType.PLUS:
            return left + right
        elif op == TokenType.MINUS:
            return left - right
        elif op == TokenType.MUL:
            return left * right
        elif op == TokenType.DIV:
            return left / right
        elif op == TokenType.GT:
            return left > right
        elif op == TokenType.LT:
            return left < right
        elif op == TokenType.GE:
            return left >= right
        elif op == TokenType.LE:
            return left <= right
        elif op == TokenType.EQ:
            return left == right
        elif op == TokenType.NE:
            return left != right
        else:
            raise Exception(f"Unsupported operator: {op}")
