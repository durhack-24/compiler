from pprint import pprint

from compiler.nodes import Label, Node, Jump
from lex import lexer
from parse import parser

def main():
    with open('test.txt', 'r') as f:
        tokens = lexer.lex(f.read())
    ast: list[Node] = parser.parse(tokens)
    labels = {
        instr.label: i
        for i, instr in enumerate(ast)
        if isinstance(instr, Label)
    }
    pprint(ast)
    ctxt = {}
    pc = 0
    while pc < len(ast):
        instr = ast[pc]
        if isinstance(instr, Label):
            continue
        try:
            instr.eval(ctxt)
        except Jump as j:
            pc = labels[j.label]
        else:
            pc += 1



if __name__ == '__main__':
    exit(main())
