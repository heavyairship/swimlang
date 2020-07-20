# SimpleLang
#
# Grammar:
#
# E ->
# | T
# | (E)
# | UOP E
# | while(E): E
# | if(E): E else: E
# | E BOP T
#
# T ->
# | n
# | b
# | v
#
# UOP ->
# | !
# FixMe: add ++ and --
#
# BOP ->
# | &
# | |
# | =
# | !=
# | <
# | <=
# | >
# | >=
# | +
# | *
# | ;
# | :=
#
# b ->
# | True
# | False
#
# n ->
# | [0-9]+
#
# v -> (variable term)
# | [a-zA-Z]+[a-zA-Z0-9]/{True, False}

import enum

##################################################################################
# Utility functions
##################################################################################


def alpha(val):
    if val is None:
        return False
    for c in val:
        ordc = ord(c.lower())
        if ordc not in range(ord('a'), ord('z') + 1):
            return False
    return True


def numeric(val):
    if val is None:
        return False
    for c in val:
        ordc = ord(c)
        if ordc not in range(ord('0'), ord('9') + 1):
            return False
    return True


def alphanumeric(val):
    if val is None:
        return False
    for c in val:
        if not (alpha(c) or numeric(c)):
            return False
    return True


def isspace(val):
    if val is None:
        return False
    return val.isspace()

##################################################################################
# Interpreter
##################################################################################

##################################################################################
# Tokenizer
##################################################################################


@enum.unique
class TokenType(enum.Enum):
    WHILE = "while"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    COLON = ":"
    IF = "if"
    ELSE = "else"
    NOT = "!"
    AND = "&"
    OR = "|"
    EQ = "="
    NOT_EQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    ADD = "+"
    MUL = "*"
    SEQ = ";"
    ASSIGN = ":="
    TRUE = "True"
    FALSE = "False"
    INT = enum.auto()
    VAR = enum.auto()


class Token(object):
    def __init__(self, typ, val):
        if not type(typ) is TokenType:
            raise TypeError
        if type(val) not in [int, str] and val is not None:
            raise TypeError
        self.typ = typ
        self.val = val

    def __str__(self):
        return "%s%s" % (self.typ.name, "("+str(self.val)+")" if self.val is not None else "")


KEYWORDS = [
    TokenType.WHILE.value,
    TokenType.IF.value,
    TokenType.ELSE.value,
    TokenType.TRUE.value,
    TokenType.FALSE.value
]


class Tokenizer(object):
    def __init__(self, src):
        self.src = src
        self.end = len(self.src)
        self.idx = 0
        self.tokens = []

    def peek(self, n=1):
        if self.idx+n > self.end:
            return None
        return self.src[self.idx:self.idx+n]

    def at(self, n):
        if n >= self.end:
            return None
        return self.src[n]

    def next(self):
        if self.done():
            return None
        out = self.src[self.idx]
        self.idx += 1
        return out

    def done(self):
        return self.idx >= self.end

    def emit(self, typ, val=None):
        self.tokens.append(Token(typ, val))

    def match(self, s):
        n = len(s)
        if self.peek(n) == s:
            self.idx += n
            return True

    def match_keyword(self):
        for kw in KEYWORDS:
            n = len(kw)
            if self.peek(n) == kw and not alphanumeric(self.at(self.idx+n)):
                self.match(kw)
                self.emit(TokenType(kw))
                return True
        return False

    def match_int(self):
        if not numeric(self.peek()):
            return False
        num = ""
        while numeric(self.peek()):
            num += self.next()
        if alpha(self.peek()):
            raise ValueError
        self.emit(TokenType.INT, int(num))
        return True

    def match_var(self):
        if not alpha(self.peek()):
            return False
        var = ""
        while alphanumeric(self.peek()):
            var += self.next()
        self.emit(TokenType.VAR, var)
        return True

    def match_space(self):
        found_space = False
        while isspace(self.peek()):
            self.next()
            found_space = True
        return found_space

    def tokenize(self):
        if self.done():
            return None
        while not self.done():
            if self.match(TokenType.NOT_EQ.value):
                self.emit(TokenType.NOT_EQ)
            elif self.match(TokenType.LTE.value):
                self.emit(TokenType.LTE)
            elif self.match(TokenType.GTE.value):
                self.emit(TokenType.GTE)
            elif self.match(TokenType.ASSIGN.value):
                self.emit(TokenType.ASSIGN)
            elif self.match(TokenType.LEFT_PAREN.value):
                self.emit(TokenType.LEFT_PAREN)
            elif self.match(TokenType.RIGHT_PAREN.value):
                self.emit(TokenType.RIGHT_PAREN)
            elif self.match(TokenType.COLON.value):
                self.emit(TokenType.COLON)
            elif self.match(TokenType.NOT.value):
                self.emit(TokenType.NOT)
            elif self.match(TokenType.AND.value):
                self.emit(TokenType.AND)
            elif self.match(TokenType.OR.value):
                self.emit(TokenType.OR)
            elif self.match(TokenType.EQ.value):
                self.emit(TokenType.EQ)
            elif self.match(TokenType.LT.value):
                self.emit(TokenType.LT)
            elif self.match(TokenType.GT.value):
                self.emit(TokenType.GT)
            elif self.match(TokenType.ADD.value):
                self.emit(TokenType.ADD)
            elif self.match(TokenType.MUL.value):
                self.emit(TokenType.MUL)
            elif self.match(TokenType.SEQ.value):
                self.emit(TokenType.SEQ)
            elif self.match_keyword():
                pass
            elif self.match_var():
                pass
            elif self.match_int():
                pass
            elif self.match_space():
                pass
            else:
                raise ValueError
        tokens = self.tokens
        return tokens

##################################################################################
# Parser/AST generator
##################################################################################


class Parser(object):
    first_b = frozenset([
        TokenType.TRUE,
        TokenType.FALSE
    ])
    first_T = frozenset([
        TokenType.INT,
        TokenType.VAR]).union(first_b)
    first_UOP = frozenset([TokenType.NOT])
    first_BOP = frozenset([
        TokenType.AND,
        TokenType.OR,
        TokenType.EQ,
        TokenType.NOT_EQ,
        TokenType.LT,
        TokenType.LTE,
        TokenType.GT,
        TokenType.GTE,
        TokenType.ADD,
        TokenType.MUL,
        TokenType.SEQ,
        TokenType.ASSIGN])

    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0

    def done(self):
        return self.idx >= len(self.tokens)

    def match(self, t):
        if self.done():
            raise ValueError
        out = tokens[self.idx]
        if out.typ != t:
            raise ValueError
        self.idx += 1
        return out

    def lookahead(self):
        if self.done():
            return None
        return tokens[self.idx].typ

    def E_helper(self):
        l = self.lookahead()
        if l in Parser.first_T:
            t = self.T()
            return t
        elif l == TokenType.LEFT_PAREN:
            self.match(TokenType.LEFT_PAREN)
            e = self.E()
            self.match(TokenType.RIGHT_PAREN)
            return e
        elif l in Parser.first_UOP:
            uop = self.UOP()
            e = self.E()
            return uop(t)
        elif l == TokenType.WHILE:
            self.match(TokenType.WHILE)
            self.match(TokenType.LEFT_PAREN)
            e = self.E()
            self.match(TokenType.RIGHT_PAREN)
            self.match(TokenType.COLON)
            e2 = self.E()
            return While(e, e2)
        elif l == TokenType.IF:
            self.match(TokenType.IF)
            self.match(TokenType.LEFT_PAREN)
            e = self.E()
            self.match(TokenType.RIGHT_PAREN)
            self.match(TokenType.COLON)
            e2 = self.E()
            self.match(TokenType.ELSE)
            self.match(TokenType.COLON)
            e3 = self.E()
            return If(e, e2, e3)
        else:
            raise ValueError

    def E(self):
        e = self.E_helper()
        while self.lookahead() in Parser.first_BOP:
            bop = self.BOP()
            e2 = self.E_helper()
            e = bop(e, e2)
        if self.lookahead() is None:
            return e
        else:
            raise ValueError

        while True:
            e = self.E_helper()
            l = self.lookahead()
            if l in Parser.first_BOP:
                bop = self.BOP()
                e2 = self.E_helper()
                e = bop(e, e2)
            elif l is None:
                return e
            else:
                raise ValueError

    def T(self):
        l = self.lookahead()
        if l == TokenType.INT:
            n = self.match(TokenType.INT)
            return Int(n.val)
        elif l in Parser.first_b:
            b = self.b()
            return Bool(b)
        elif l == TokenType.VAR:
            v = self.match(TokenType.VAR)
            return Var(v.val)
        else:
            raise ValueError

    def UOP(self):
        l = self.lookahead()
        if l == TokenType.NOT:
            self.match(TokenType.NOT)
            return Not
        else:
            raise ValueError

    def BOP(self):
        l = self.lookahead()
        if l == TokenType.AND:
            self.match(TokenType.AND)
            return And
        elif l == TokenType.OR:
            self.match(TokenType.OR)
            return Or
        elif l == TokenType.EQ:
            self.match(TokenType.EQ)
            return Eq
        elif l == TokenType.NOT_EQ:
            self.match(TokenType.NOT_EQ)
            return NotEq
        elif l == TokenType.LT:
            self.match(TokenType.LT)
            return Lt
        elif l == TokenType.LTE:
            self.match(TokenType.LTE)
            return Lte
        elif l == TokenType.GT:
            self.match(TokenType.GT)
            return Gt
        elif l == TokenType.GTE:
            self.match(TokenType.GTE)
            return Gte
        elif l == TokenType.ADD:
            self.match(TokenType.ADD)
            return Add
        elif l == TokenType.MUL:
            self.match(TokenType.MUL)
            return Mul
        elif l == TokenType.SEQ:
            self.match(TokenType.SEQ)
            return Seq
        elif l == TokenType.ASSIGN:
            self.match(TokenType.ASSIGN)
            return Assign
        else:
            raise ValueError

    def b(self):
        l = self.lookahead()
        if l == TokenType.TRUE:
            self.match(TokenType.TRUE)
            return True
        elif l == TokenType.FALSE:
            self.match(TokenType.FALSE)
            return False

    def parse(self):
        if self.done():
            return None
        return self.E()

##################################################################################
# AST types
##################################################################################


class Node(object):
    def accept(self, visitor):
        pass


class Int(Node):
    def __init__(self, val):
        if not type(val) is int:
            raise TypeError
        self.val = val

    def accept(self, visitor):
        return visitor.visit_int(self)


class Add(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_add(self)


class Mul(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_mul(self)


class Eq(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_eq(self)


class NotEq(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_not_eq(self)


class Lt(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_lt(self)


class Lte(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_lte(self)


class Gt(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_gt(self)


class Gte(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_gte(self)


class Bool(Node):
    def __init__(self, val):
        if not type(val) is bool:
            raise TypeError
        self.val = val

    def accept(self, visitor):
        return visitor.visit_bool(self)


class And(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_and(self)


class Or(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_or(self)


class Not(Node):
    def __init__(self, arg):
        if not issubclass(type(arg), Node):
            raise TypeError
        self.arg = arg

    def accept(self, visitor):
        return visitor.visit_not(self)


class If(Node):
    def __init__(self, cond, first, second):
        if not (issubclass(type(cond), Node) and issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.cond = cond
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_if(self)


class While(Node):
    def __init__(self, cond, body):
        if not (issubclass(type(cond), Node) and issubclass(type(body), Node)):
            raise TypeError
        self.cond = cond
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while(self)


class Assign(Node):
    def __init__(self, var, expr):
        if not type(var) is Var:
            raise TypeError
        if not issubclass(type(expr), Node):
            raise TypeError
        self.var = var
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_assign(self)


class Var(Node):
    def __init__(self, val):
        if not type(val) is str:
            raise TypeError
        if not alpha(val):
            raise TypeError
        self.val = val

    def accept(self, visitor):
        return visitor.visit_var(self)


class Seq(Node):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_seq(self)

##################################################################################
# Visitor base class
##################################################################################


class Visitor(object):
    def __call__(self, node):
        return node.accept(self)

    def visit_int(self, node):
        raise NotImplementedError

    def visit_add(self, node):
        raise NotImplementedError

    def visit_mul(self, node):
        raise NotImplementedError

    def visit_eq(self, node):
        raise NotImplementedError

    def visit_not_eq(self, node):
        raise NotImplementedError

    def visit_lt(self, node):
        raise NotImplementedError

    def visit_lte(self, node):
        raise NotImplementedError

    def visit_gt(self, node):
        raise NotImplementedError

    def visit_gte(self, node):
        raise NotImplementedError

    def visit_bool(self, node):
        raise NotImplementedError

    def visit_and(self, node):
        raise NotImplementedError

    def visit_or(self, node):
        raise NotImplementedError

    def visit_if(self, node):
        raise NotImplementedError

    def visit_not(self, node):
        raise NotImplementedError

    def visit_while(self, node):
        raise NotImplementedError

    def visit_assign(self, node):
        raise NotImplementedError

    def visit_var(self, node):
        raise NotImplementedError

    def visit_seq(self, node):
        raise NotImplementedError

##################################################################################
# AST printer
##################################################################################


class Printer(Visitor):
    def __init__(self):
        self.indent = ""

    def visit_int(self, node):
        if not type(node) is Int:
            raise TypeError
        return str(node.val)

    def visit_add(self, node):
        if not type(node) is Add:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '+', self(node.second))

    def visit_mul(self, node):
        if not type(node) is Mul:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '*', self(node.second))

    def visit_eq(self, node):
        if not type(node) is Eq:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '==', self(node.second))

    def visit_not_eq(self, node):
        if not type(node) is NotEq:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '!=', self(node.second))

    def visit_lt(self, node):
        if not type(node) is Lt:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '<', self(node.second))

    def visit_lte(self, node):
        if not type(node) is Lte:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '<=', self(node.second))

    def visit_gt(self, node):
        if not type(node) is Gt:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '>', self(node.second))

    def visit_gte(self, node):
        if not type(node) is Gte:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '>=', self(node.second))

    def visit_bool(self, node):
        if not type(node) is Bool:
            raise TypeError
        return str(node.val)

    def visit_and(self, node):
        if not type(node) is And:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '&', self(node.second))

    def visit_or(self, node):
        if not type(node) is Or:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), '|', self(node.second))

    def visit_if(self, node):
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

    def visit_not(self, node):
        if not type(node) is Not:
            raise TypeError
        return '!%s' % self(node.arg)

    def visit_while(self, node):
        if not type(node) is While:
            raise TypeError
        cond = self(node.cond)
        indent = self.indent
        self.indent = indent + "  "
        body = self(node.body)
        self.indent = indent
        return 'while(' + cond + '):\n' + indent + '  ' + body

    def visit_assign(self, node):
        if not type(node) is Assign:
            raise TypeError
        return "%s := %s" % (self(node.var), self(node.expr))

    def visit_var(self, node):
        if not type(node) is Var:
            raise TypeError
        return node.val

    def visit_seq(self, node):
        if not type(node) is Seq:
            raise TypeError
        return "%s;\n%s%s" % (self(node.first), self.indent, self(node.second))

##################################################################################
# AST evaluator
##################################################################################


class Evaluator(Visitor):
    state = {}

    def visit_int(self, node):
        if not type(node) is Int:
            raise TypeError
        return node.val

    def visit_add(self, node):
        if not type(node) is Add:
            raise TypeError
        return self(node.first) + self(node.second)

    def visit_mul(self, node):
        if not type(node) is Mul:
            raise TypeError
        return self(node.first) * self(node.second)

    def visit_eq(self, node):
        if not type(node) is Eq:
            raise TypeError
        return self(node.first) == self(node.second)

    def visit_not_eq(self, node):
        if not type(node) is NotEq:
            raise TypeError
        return self(node.first) != self(node.second)

    def visit_lt(self, node):
        if not type(node) is Lt:
            raise TypeError
        return self(node.first) < self(node.second)

    def visit_lte(self, node):
        if not type(node) is Lte:
            raise TypeError
        return self(node.first) <= self(node.second)

    def visit_gt(self, node):
        if not type(node) is Gt:
            raise TypeError
        return self(node.first) > self(node.second)

    def visit_gte(self, node):
        if not type(node) is Gte:
            raise TypeError
        return self(node.first) >= self(node.second)

    def visit_bool(self, node):
        if not type(node) is Bool:
            raise TypeError
        return node.val

    def visit_and(self, node):
        if not type(node) is And:
            raise TypeError
        return self(node.first) and self(node.second)

    def visit_or(self, node):
        if not type(node) is Or:
            raise TypeError
        return self(node.first) or self(node.second)

    def visit_not(self, node):
        if not type(node) is Not:
            raise TypeError
        return not self(node.arg)

    def visit_if(self, node):
        if not type(node) is If:
            raise TypeError
        return self(node.first) if self(node.cond) else self(node.second)

    def visit_while(self, node):
        if not type(node) is While:
            raise TypeError
        out = False
        while(self(node.cond)):
            out = self(node.body)
        return out

    def visit_assign(self, node):
        if not type(node) is Assign:
            raise TypeError
        Evaluator.state[node.var.val] = self(node.expr)
        return Evaluator.state[node.var.val]

    def visit_var(self, node):
        if not type(node) is Var:
            raise TypeError
        return Evaluator.state[node.val]

    def visit_seq(self, node):
        if not type(node) is Seq:
            raise TypeError
        self(node.first)
        return self(node.second)

##################################################################################
# AST type checker
##################################################################################


class TypeChecker(Visitor):
    # FixMe: implement
    pass

##################################################################################
# Main
##################################################################################


if __name__ == "__main__":
    visitors = [Printer(), Evaluator()]

    # Test arithmetic/bool statements
    print("**********")
    node1 = Mul(Int(2), Int(3))  # 6
    node2 = Add(Int(2), Int(3))  # 5
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
    node6 = Seq(node1, node2)
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

    src = """
    whileb := 10;
    if(whileb >= 0):
        x := 1;
        y := 2 > 1
    else:
        p := 1 + 1;
        z := 2 > 2"""
    src = "whileb := 10; whileb"
    tokenizer = Tokenizer(src)
    tokens = tokenizer.tokenize()
    print(src)
    print("[")
    for t in tokens:
        print("\t" + t.typ.name + ("("+str(t.val)+")" if t.val or t.val == 0 else ""))
    print("]")
    print("**********")
    parser = Parser(tokens)
    node = parser.parse()
    for v in visitors:
        print(v(node))
