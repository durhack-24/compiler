from rply import LexerGenerator

lg = LexerGenerator()

lg.add('OPCODE',   r'O\d+')
lg.add('VARIABLE', r'V\d+')
lg.add('DATA',     r'D-?\d+')
lg.add('LABEL',    r'L[a-zA-Z0-9]+')
lg.add('NUM',      r'-?\d+')

lg.ignore(r'\s+')

lexer = lg.build()
