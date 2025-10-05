import lexer

class ASTNode: pass

class Program(ASTNode):
    def __init__(self, statements): self.statements = statements
    def __repr__(self): return f"Program({self.statements})"

class PokemonDecl(ASTNode):
    def __init__(self, name): self.name = name
    def __repr__(self): return f"PokemonDecl({self.name})"

class PrintStmt(ASTNode):
    def __init__(self, expr): self.expr = expr
    def __repr__(self): return f"Print({self.expr})"

class Assign(ASTNode):
    def __init__(self, name, expr): self.name, self.expr = name, expr
    def __repr__(self): return f"Assign({self.name} = {self.expr})"

class Identifier(ASTNode):
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Identifier({self.name})"

class Number(ASTNode):
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Number({self.value})"

class BinaryOp(ASTNode):
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
    def __repr__(self): return f"BinaryOp({self.left}, {self.op}, {self.right})"

class IfStmt(ASTNode):
    def __init__(self, condition, body, elif_blocks=None, else_body=None):
        self.condition = condition
        self.body = body
        self.elif_blocks = elif_blocks or []
        self.else_body = else_body

    def __repr__(self):
        return f"If({self.condition}, {self.body}, Elif={self.elif_blocks}, Else={self.else_body})"

"""Parser"""

class Parser:
    def __init__(self, tokens): self.tokens, self.pos = tokens, 0
    def current(self): return self.tokens[self.pos]
    def eat(self, type_=None):
        tok = self.current()
        if type_ and tok.type != type_:
            raise Exception(f"Expected {type_}, got {tok.type}")
        self.pos += 1
        return tok

    def parse(self):
        stmts = []
        while self.current().type != lexer.TokenType.EOF:
            stmts.append(self.statement())
        return Program(stmts)

    def statement(self):
        tok = self.current()

        if tok.type == lexer.TokenType.POKEMON:
            self.eat(lexer.TokenType.POKEMON)
            name = self.eat(lexer.TokenType.IDENTIFIER).value
            return PokemonDecl(name)

        if tok.type == lexer.TokenType.PRINT:
            self.eat(lexer.TokenType.PRINT)
            expr = self.expr()
            return PrintStmt(expr)

        if tok.type == lexer.TokenType.SET:
            self.eat(lexer.TokenType.SET)
            name = self.eat(lexer.TokenType.IDENTIFIER).value
            self.eat(lexer.TokenType.ASSIGN)
            expr = self.expr()
            return Assign(name, expr)

        if tok.type == lexer.TokenType.IDENTIFIER:
            name = self.eat(lexer.TokenType.IDENTIFIER).value
            if self.current().type == lexer.TokenType.ASSIGN:
                self.eat(lexer.TokenType.ASSIGN)
                expr = self.expr()
                return Assign(name, expr)
            else:
                raise Exception(f"Unexpected token after identifier: {self.current()}")

        if tok.type == lexer.TokenType.IF:
            return self.if_statement()

        raise Exception(f"Unknown statement {tok}")

    def if_statement(self):
        self.eat(lexer.TokenType.IF)
        condition = self.expr()
        body = []
        while self.current().type not in (lexer.TokenType.ELSE, lexer.TokenType.END, lexer.TokenType.IF):
            body.append(self.statement())

        elif_blocks = []
        else_body = None

        while self.current().type == lexer.TokenType.ELSE:
            self.eat(lexer.TokenType.ELSE)
            if self.current().type == lexer.TokenType.IF:
                # ELSE IF branch
                self.eat(lexer.TokenType.IF)
                cond = self.expr()
                elif_body = []
                while self.current().type not in (lexer.TokenType.ELSE, lexer.TokenType.END):
                    elif_body.append(self.statement())
                elif_blocks.append((cond, elif_body))
            else:
                # ELSE branch
                else_body = []
                while self.current().type != lexer.TokenType.END:
                    else_body.append(self.statement())
                break

        self.eat(lexer.TokenType.END)
        return IfStmt(condition, body, elif_blocks, else_body)

    """Expressions"""

    def expr(self): return self.logic_expr()

    def logic_expr(self):
        node = self.comp_expr()
        while self.current().type in (lexer.TokenType.AND, lexer.TokenType.OR):
            op = self.eat().type
            right = self.comp_expr()
            node = BinaryOp(node, op, right)
        return node

    def comp_expr(self):
        node = self.term()
        while self.current().type in (lexer.TokenType.EQ, lexer.TokenType.NE, lexer.TokenType.GT, lexer.TokenType.LT, lexer.TokenType.GE, lexer.TokenType.LE):
            op = self.eat().type
            right = self.term()
            node = BinaryOp(node, op, right)
        return node

    def term(self):
        node = self.factor()
        while self.current().type in (lexer.TokenType.PLUS, lexer.TokenType.MINUS):
            op = self.eat().type
            right = self.factor()
            node = BinaryOp(node, op, right)
        return node

    def factor(self):
        node = self.primary()
        while self.current().type in (lexer.TokenType.MUL, lexer.TokenType.DIV):
            op = self.eat().type
            right = self.primary()
            node = BinaryOp(node, op, right)
        return node

    def primary(self):
        tok = self.current()
        if tok.type == lexer.TokenType.NUMBER: return Number(self.eat().value)
        if tok.type == lexer.TokenType.IDENTIFIER: return Identifier(self.eat().value)
        raise Exception(f"Unexpected token {tok}")
