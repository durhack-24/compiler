from rply import ParserGenerator

from compiler.nodes import SetArr
from nodes import Variable, Constant, Print

pg = ParserGenerator(
    [
        'OPCODE',
        'VARIABLE',
        'DATA',
        'LABEL',
        'NUM',
    ],
    precedence=[]
)


@pg.production('program : instruction')
@pg.production('program : program instruction')
def program(p):
    if len(p) == 1:
        return [p[0]]
    return p[0] + [p[1]]


@pg.production('variable : VARIABLE')
def variable(p):
    return Variable(int(p[0].value[1:]))


@pg.production('data : DATA')
def constant(p):
    return Constant(int(p[0].value[1:]))


@pg.production('parameter : variable')
@pg.production('parameter : data')
def parameter(p):
    return p[0]


@pg.production('instruction : OPCODE nums')
def jump(p):
    print(p)
    return p


@pg.production('nums : data')
@pg.production('nums : nums data')
def nums(p):
    if len(p) == 1:
        return [p[0]]
    return p[0] + [p[1]]


@pg.production('instruction : OPCODE parameter')
def var_param(p):
    opcode, var = p
    match opcode.value:
        case 'O12':
            return Print(var)
    print(p)
    return p


@pg.production('instruction : OPCODE parameter parameter parameter')
def tri_op(p):
    opcode, a, b, c = p
    match opcode.value:
        case 'O15':
            return SetArr(a, b, c)
    print(p)
    return p


parser = pg.build()
