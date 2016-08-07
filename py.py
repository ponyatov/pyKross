# generic object

class Object:
    'generic object'
    tag = 'obj'
    def __init__(self, val): self.val = val
    def __repr__(self):
        return '<%s:%s:%s>' % (self.tag, self.val, self.val.__class__.__name__)

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
    
# scalars
    
class Symbol(Scalar):
    'superscalar type can represent any scalar value: label, number, string,..'
    tag = 'sym'
    
class String(Scalar):
    tag = 'str'

class AnyNumber(Scalar):
    'superclass for any numeric types'
    tag = 'number'
class Num(AnyNumber):
    tag = 'num'
class Int(AnyNumber):
    tag = 'int'
class Hex(Int):
    tag = 'hex'

print Symbol('symsym'),Int('123'),Num(456),Symbol(-4e+5)
