import lexer
import parser
from interpreter import MiniLang

if __name__ == "__main__":
    with open("program.mini", "r") as f:
        code = f.read()

    lex = lexer.Lexer(code)
    tokens = lex.get_tokens()

    print(tokens)  # print tokens for debugging

    parse = parser.Parser(tokens)
    tree = parse.parse()

    print(tree)  # print AST for debugging

    interpreter = MiniLang()
    interpreter.execute(tree) # executes program.mini
