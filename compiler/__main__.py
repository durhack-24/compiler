from pprint import pprint

from lex import lexer
from parse import parser

def main():
    with open('test.txt', 'r') as f:
        tokens = lexer.lex(f.read())
    ast = parser.parse(tokens)
    pprint(ast)
    ctxt = {}
    for instr in ast:
        instr.eval(ctxt)


if __name__ == '__main__':
    exit(main())
