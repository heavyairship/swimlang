# SimpleLang
#
# Grammar:
#
# E -> (expressions)
# | (E)
# | B
# | A
# | while(B): E
# | if(B): E else: E
# | V := E
# | E; E
#
# B -> (boolean expressions)
# | True
# | False
# | V
# | (B & B)
# | (B | B)
# | !B
# | (A = A)
# | (A != A)
# | (A < A)
# | (A <= A)
# | (A > A)
# | (A >= A)
#
# A -> (arithmetic expressions)
# | N
# | V
# | (A + A)
# | (A * A)
#
# V -> (variable expressions)
# | [a-zA-Z0-9]+

class SLVisitor(object):
    def visitAdd(self, node):
        pass
    def visitMul(self, node):
        pass
    def __call__(self, node):
        return node.accept(self)

class SLPrinter(SLVisitor):
    def __init__(self):
        self.indent = ""
    def visitInt(self, node):
        if not type(node) is Int:
            raise TypeError
        return str(node.val)
    def visitAdd(self, node):
        if not type(node) is Add:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '+', self(node.second))
    def visitMul(self, node):
        if not type(node) is Mul:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '*', self(node.second))
    def visitEq(self, node):
        if not type(node) is Eq:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '==', self(node.second))
    def visitNotEq(self, node):
        if not type(node) is NotEq:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '!=', self(node.second))
    def visitLt(self, node):
        if not type(node) is Lt:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '<', self(node.second))
    def visitLte(self, node):
        if not type(node) is Lte:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '<=', self(node.second))
    def visitGt(self, node):
        if not type(node) is Gt:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '>', self(node.second))
    def visitGte(self, node):
        if not type(node) is Gte:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '>=', self(node.second))
    def visitBool(self, node):
        if not type(node) is Bool:
            raise TypeError
        return str(node.val)
    def visitAnd(self, node):
        if not type(node) is And:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '&', self(node.second))
    def visitOr(self, node):
        if not type(node) is Or:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '|', self(node.second))
    def visitIf(self, node):
        if not type(node) is If:
            raise TypeError
        cond = self(node.cond)
        indent = self.indent
        self.indent = indent + "  "
        tbranch = self(node.first)
        self.indent = indent + "  "
        fbranch = self(node.second)
        self.indent = indent
        return 'if(' + cond + '):\n' + indent + '  ' + tbranch + '\n' + indent + 'else:\n' + indent + '  ' + fbranch 
    def visitNot(self, node):
        if not type(node) is Not:
            raise TypeError
        return '!%s' % self(node.arg)
    def visitWhile(self, node):
        if not type(node) is While:
            raise TypeError
        cond = self(node.cond)
        indent = self.indent
        self.indent = indent + "  "
        body = self(node.body)
        self.indent = indent
        return 'while(' + cond + '):\n' + indent + '  ' + body
    def visitAssign(self, node):
        if not type(node) is Assign:
            raise TypeError
        return "%s = %s" % (self(node.var), self(node.expr))
    def visitVar(self, node):
        if not type(node) is Var:
            raise TypeError
        return node.val
    def visitSeq(self, node):
        if not type(node) is Seq:
            raise TypeError
        return "%s;\n%s" % (self(node.first), self(node.second))

class SLEvaluator(SLVisitor):
    state = {}
    def visitInt(self, node):
        if not type(node) is Int:
            raise TypeError
        return node.val
    def visitAdd(self, node):
        if not type(node) is Add:
            raise TypeError
        return self(node.first) + self(node.second)
    def visitMul(self, node):
        if not type(node) is Mul:
            raise TypeError
        return self(node.first) * self(node.second)
    def visitEq(self, node):
        if not type(node) is Eq:
            raise TypeError
        return self(node.first) == self(node.second)
    def visitNotEq(self, node):
        if not type(node) is NotEq:
            raise TypeError
        return self(node.first) != self(node.second)
    def visitLt(self, node):
        if not type(node) is Lt:
            raise TypeError
        return self(node.first) < self(node.second)
    def visitLte(self, node):
        if not type(node) is Lte:
            raise TypeError
        return self(node.first) <= self(node.second)
    def visitGt(self, node):
        if not type(node) is Gt:
            raise TypeError
        return self(node.first) > self(node.second)
    def visitGte(self, node):
        if not type(node) is Gte:
            raise TypeError
        return self(node.first) >= self(node.second)
    def visitBool(self, node):
        if not type(node) is Bool:
            raise TypeError
        return node.val
    def visitAnd(self, node):
        if not type(node) is And:
            raise TypeError
        return self(node.first) and self(node.second)
    def visitOr(self, node):
        if not type(node) is Or:
            raise TypeError
        return self(node.first) or self(node.second)
    def visitNot(self, node):
        if not type(node) is Not:
            raise TypeError
        return not self(node.arg)
    def visitIf(self, node):
        if not type(node) is If:
            raise TypeError
        return self(node.first) if self(node.cond) else self(node.second)
    def visitWhile(self, node):
        if not type(node) is While:
            raise TypeError
        out = False
        while(self(node.cond)):
            out = self(node.body)
        return out
    def visitAssign(self, node):
        if not type(node) is Assign:
            raise TypeError
        SLEvaluator.state[node.var.val] = self(node.expr)
        return SLEvaluator.state[node.var.val]
    def visitVar(self, node):
        if not type(node) is Var:
            raise TypeError
        return SLEvaluator.state[node.val]
    def visitSeq(self, node):
        if not type(node) is Seq:
            raise TypeError
        self(node.first)
        return self(node.second)

class Node(object):
    def accept(self, visitor):
        pass
    def numeric(self, o):
        return type(o) in [Int, Add, Mul, Var]
    def boolean(self, o):
        return type(o) in [Eq, NotEq, Lt, Lte, Gt, Gte, Bool, And, Or, Not, Var]

class Int(Node):
    def __init__(self, val):
        if not type(val) is int:
            raise TypeError
        self.val = val
    def accept(self, visitor):
        return visitor.visitInt(self)

class Add(Node):
    def __init__(self, first, second):
        if not (self.numeric(first) and self.numeric(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitAdd(self)

class Mul(Node):
    def __init__(self, first, second):
        if not (self.numeric(first) and self.numeric(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitMul(self)

class Eq(Node):
    def __init__(self, first, second):
        if not (self.numeric(first) and self.numeric(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitEq(self)

class NotEq(Node):
    def __init__(self, first, second):
        if not (self.numeric(first) and self.numeric(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitNotEq(self)

class Lt(Node):
    def __init__(self, first, second):
        if not (self.numeric(first) and self.numeric(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitLt(self)

class Lte(Node):
    def __init__(self, first, second):
        if not (self.numeric(first) and self.numeric(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitLte(self)

class Gt(Node):
    def __init__(self, first, second):
        if not (self.numeric(first) and self.numeric(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitGt(self)

class Gte(Node):
    def __init__(self, first, second):
        if not (self.numeric(first) and self.numeric(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitGte(self)

class Bool(Node):
    def __init__(self, val):
        if not type(val) is bool:
            raise TypeError
        self.val = val
    def accept(self, visitor):
        return visitor.visitBool(self)

class And(Node):
    def __init__(self, first, second):
        if not (self.boolean(first) and self.boolean(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitAnd(self)

class Or(Node):
    def __init__(self, first, second):
        if not (self.boolean(first) and self.boolean(second)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitOr(self)

class Not(Node):
    def __init__(self, arg):
        if not (self.boolean(arg)):
            raise TypeError
        self.arg = arg
    def accept(self, visitor):
        return visitor.visitNot(self)

class If(Node):
    def __init__(self, cond, first, second):
        if not self.boolean(cond):
            raise TypeError
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.cond = cond
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitIf(self)

class While(Node):
    def __init__(self, cond, body):
        if not self.boolean(cond):
            raise TypeError
        if not issubclass(type(body), Node):
            raise TypeError
        self.cond = cond
        self.body = body
    def accept(self, visitor):
        return visitor.visitWhile(self)

class Assign(Node):
    def __init__(self, var, expr):
        if not type(var) is Var:
            raise TypeError
        if not issubclass(type(expr), Node):
            raise TypeError
        self.var = var
        self.expr = expr
    def accept(self, visitor):
        return visitor.visitAssign(self)

class Var(Node):
    def __init__(self, val):
        if not type(val) is str:
            raise TypeError
        for c in val:
            ordc = ord(c.lower())
            alpha = ordc in range(ord('a'), ord('z') + 1)
            numeric = ordc in range(ord('0'), ord('9') + 1)
            if not (alpha or numeric):
                raise TypeError
        self.val = val
    def accept(self, visitor):
        return visitor.visitVar(self)

class Seq(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second
    def accept(self, visitor):
        return visitor.visitSeq(self)

class SLTypeChecker(object):
    # TODO: implement!
    pass

class SLParser(object):
    # TODO: implement!
    pass

if __name__ == "__main__":
    visitors = [SLPrinter(), SLEvaluator()]

    # Test arithmetic/bool statements
    print("**********")
    node1 = Mul(Int(2), Int(3)) # 6
    node2 = Add(Int(2),Int(3)) # 5
    node3 = Add(node1, Mul(node1, node2))
    node4 = Eq(Int(31), node3)
    node5 = Or(node4, Eq(Int(1), Int(1)))
    node6 = And(Not(node5), node5)
    for v in visitors:
        print(v(node6))

    # Test if statements
    print("**********")
    node1 = If(Bool(True), Bool(True), Int(2))
    node2 = If(Bool(False), node1, Int(3))
    node3 = If(Bool(True), node2, node2)
    for v in visitors:
        print(v(node2))

    # Test assign
    print("**********")
    node1 = Assign(Var("x"), Add(Int(1), Int(1)))
    for v in visitors:
        print(v(node1))

    # Test seq
    print("**********")
    node1 = Assign(Var("x"), Add(Int(1), Int(1)))
    node2 = Assign(Var("b"), Bool(True))
    node3 = Assign(Var("y"), Add(Var("x"), Int(10)))
    node4 = Assign(Var("y"), Add(Var("x"), Int(20)))
    node5 = If(Var("b"), node3, node4)
    node6 = Seq(node1, node2);
    node7 = Seq(node5, Var("y"))
    node8 = Seq(node6, node7)
    for v in visitors:
        print(v(node8))

    # Test while statements
    print("**********")
    node1 = Assign(Var("x"), Int(0))
    node2 = Assign(Var("x"), Add(Var("x"), Int(1)))
    node3 = While(NotEq(Var("x"), Int(10)), node2) 
    node4 = Seq(node1, node3)
    for v in visitors:
        print(v(node4))
