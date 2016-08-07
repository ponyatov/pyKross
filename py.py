# generic object

# misc
def pad(val, width):
    V = str(val) ; W = width - len(V)
    return V + ' ' * W

class Object:
    'generic object'
    tag = 'obj'
    def __init__(self, val): self.val = val
    def __repr__(self):
        return '<%s:%s:%s>' % (self.tag, self.val, self.val.__class__.__name__)
    # krosstranslation
    def c(self):
        'in pure C89'
        return '%s' % self.val
    def cpp(self):
        'in GNU++11 C++'
        return c()
    lex = 'error(LEX-ERROR)'
    def lex_TOC(self):
        C = self.__class__.__name__
        return 'TOC(%s,%s)'%(C,C.upper())
    def flex(self):
        'in Lex/Flex'
        return '%s%s%s\n'%(
            pad(self.lex,20),
            pad(self.lex_TOC(),20),
            pad('/* '+self.__class__.__doc__,40-4)+' */')
    yacc = 'error(YACC-ERROR)'
    def bison(self):
        'in Yacc/Bison'
        return self.yacc

# superclasses

class Scalar(Object):
    'scalar item'
    tag = 'scalar'
class Composite(Object):
    'composite item composed from other objects'
    tag = 'composite'
class Pointer(Object):
    'pointer to other object'
    tag = 'ptr'
    
# documentation

class Doc(Object):
    'some documentation info'
    tag = 'doc'
class LineComment(Doc):
    'line comment'
    tag = 'comment'
    lex = r'#[^\n]*\n'
    def lex_TOC(self): return '{}'
class SyntaxSpaces(Doc):
    'drop spaces'
    lex = r''
    def lex_TOC(self): return '{}'
    
# scalars
    
class Symbol(Scalar):
    'universal symbolic type'
    tag = 'sym'
    lex = r'[a-zA-Z{N}_]+'
    def __init__(self,val): self.val = str(val)
    
class String(Scalar):
    'string'
    tag = 'str'
    lex = r"'.*'"
    def __init__(self,val): self.val = str(val)

class AnyNumber(Scalar):
    'superclass for any numeric types'
    tag = 'number'
class Num(AnyNumber):
    'floating point number'
    tag = 'num'
    lex = r'{S}{N}\.{N}'
    def __init__(self,val): self.val = float(val)
    def c(self): return '((float)%s)'%self.val
class Int(AnyNumber):
    'integer number'
    tag = 'int'
    lex = r'{S}{N}'
    def __init__(self,val): self.val = int(val)
    def c(self): return '((int)%s)'%self.val
class Hex(Int):
    'fixed width hexadecimal number'
    tag = 'hex'
    lex = r'0x[{N}A-F]+'

dat = [
       Symbol('symsym'), Num(456), Symbol(-4e+5), Hex(0x1234), Int('123')
       ]

# syntax lexer/parser generators

def lex():
    'return contents of lpp.lpp file (flex lexer)'
    S = '%{\n#include "hpp.hpp"\n%}\n'+\
        '%option noyywrap yylineno\n'+\
        'S [\+\-]?\nN [0-9]+\n'+\
        '%%\n'
    for i in [
              LineComment(''),String(''),Symbol('sym'),
              Num(0),Hex(0),Int(0),
              SyntaxSpaces('')
              ]: S += i.flex()
    S += '%%\n'
    return S

print 'Y:'
for i in dat: print i,
print '\nC89:'
for i in dat: print i.c(),
print '\nLex: '
print lex()
