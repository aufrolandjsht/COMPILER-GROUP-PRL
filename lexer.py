from enum import Enum, auto

"""Define Tokens with Enum"""

class TokenType(Enum):
    # Keywords
    POKEMON = auto()
    PRINT = auto()
    SEARCH = auto()
    SET = auto()
    END = auto()

    # Conditionals
    IF = auto()
    ELSE = auto()

    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()

    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # Operators
    ASSIGN = auto()  # =
    EQ = auto()      # ==
    NE = auto()      # !=
    GT = auto()      # >
    LT = auto()      # <
    GE = auto()      # >=
    LE = auto()      # <=
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()

    # End of file
    EOF = auto()

"""Tokenizer"""

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

"""Lexer"""

class Lexer:
    keywords = {
        "POKEMON": TokenType.POKEMON,
        "PRINT": TokenType.PRINT,
        "SEARCH": TokenType.SEARCH,
        "SET": TokenType.SET,
        "IF": TokenType.IF,
        "ELSE": TokenType.ELSE,
        "END": TokenType.END,
        "AND": TokenType.AND,
        "OR": TokenType.OR,
        "NOT": TokenType.NOT,
    }

    """Tokenization"""

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    """Token Types"""

    def identifier(self):
        result = ""
        while self.current_char and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()
        token_type = self.keywords.get(result.upper(), TokenType.IDENTIFIER)
        return Token(token_type, result)

    def number(self):
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, int(result))

    def get_tokens(self):
        tokens = []
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                tokens.append(self.identifier())
                continue
            if self.current_char.isdigit():
                tokens.append(self.number())
                continue

            # Operators
            if self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    tokens.append(Token(TokenType.EQ))
                else:
                    tokens.append(Token(TokenType.ASSIGN))
                continue
            if self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    tokens.append(Token(TokenType.NE))
                continue
            if self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    tokens.append(Token(TokenType.GE))
                else:
                    tokens.append(Token(TokenType.GT))
                continue
            if self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    tokens.append(Token(TokenType.LE))
                else:
                    tokens.append(Token(TokenType.LT))
                continue

            # Arithmetic
            if self.current_char == "+":
                self.advance(); tokens.append(Token(TokenType.PLUS)); continue
            if self.current_char == "-":
                self.advance(); tokens.append(Token(TokenType.MINUS)); continue
            if self.current_char == "*":
                self.advance(); tokens.append(Token(TokenType.MUL)); continue
            if self.current_char == "/":
                self.advance(); tokens.append(Token(TokenType.DIV)); continue

            raise Exception(f"Unknown char: {self.current_char}")

        tokens.append(Token(TokenType.EOF))
        return tokens
