# SimpleLang
#
# Grammar:
#
# FixMe: allow extra ;
#
# E -> (expression)
# | T
# | (E)
# | UOP E
# | while(E): E end
# | if(E): E else: E end
# | E BOP T
# | func v(P): E end # FixMe: does it make sense for this to be an expression?
# | call v(A)
#
# T -> (term)
# | n
# | b
# | v
#
# P -> (param list)
# | ε
# | P2
#
# P2 -> (param list helper)
# | v P3
#
# P3 -> (param list helper)
# | ε
# | , P2
#
# A -> (arg list)
# | ε
# | A2
#
# A2 -> (arg list helper)
# | E A3
#
# A3 -> (arg list helper)
# | ε
# | , A2
#
# UOP -> (unary operation)
# | !
# FixMe: add ++ and --
#
# BOP -> (binary operation)
# | &&
# | ||
# | ==
# | !=
# | <
# | <=
# | >
# | >=
# | +
# | -
# | *
# | /
# | ;
# | :=
#
# b -> (boolean atom)
# | True
# | False
#
# n -> (integer atom)
# | [0-9]+
#
# v -> (variable atom) # FixMe: should probably distinguish b/w var/id
# | [a-zA-Z]+[a-zA-Z0-9]/{True, False}

import enum
import argparse

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


class Interpreter(object):
    def __init__(self, src):
        self.src = src

    def interpret(self, verbose=False):
        tokens = Tokenizer(self.src).tokenize()
        ast = Parser(tokens).parse()
        if verbose:
            print("\n*********************")
            print("Parsed the following:")
            print("*********************")
            print(Printer()(ast))
            print("*********************\n")
        res = Evaluator()(ast)
        return res

##################################################################################
# Tokenizer
##################################################################################


@enum.unique
class TokenType(enum.Enum):
    WHILE = "while"
    END = "end"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    COLON = ":"
    IF = "if"
    ELSE = "else"
    FUNC = "func"
    CALL = "call"
    NOT = "!"
    AND = "&&"
    OR = "||"
    EQ = "=="
    NOT_EQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    SEQ = ";"
    COMMA = ","
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
    TokenType.END.value,
    TokenType.IF.value,
    TokenType.ELSE.value,
    TokenType.FUNC.value,
    TokenType.CALL.value,
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
        return self.src[self.idx: self.idx+n]

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
            elif self.match(TokenType.SUB.value):
                self.emit(TokenType.SUB)
            elif self.match(TokenType.MUL.value):
                self.emit(TokenType.MUL)
            elif self.match(TokenType.DIV.value):
                self.emit(TokenType.DIV)
            elif self.match(TokenType.SEQ.value):
                self.emit(TokenType.SEQ)
            elif self.match(TokenType.COMMA.value):
                self.emit(TokenType.COMMA)
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
        return self.tokens

##################################################################################
# Parser/AST generator
##################################################################################


class Parser(object):
    first_b = frozenset([TokenType.TRUE, TokenType.FALSE])

    first_T = frozenset([TokenType.INT, TokenType.VAR]).union(first_b)

    first_P2 = frozenset([TokenType.VAR])

    first_P3 = frozenset([TokenType.COMMA])

    first_P = frozenset([]).union(first_P2)

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
        TokenType.SUB,
        TokenType.MUL,
        TokenType.DIV,
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
        out = self.tokens[self.idx]
        if out.typ != t:
            raise ValueError
        self.idx += 1
        return out

    def lookahead(self):
        if self.done():
            return None
        return self.tokens[self.idx].typ

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
            self.match(TokenType.END)
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
            self.match(TokenType.END)
            return If(e, e2, e3)
        elif l == TokenType.FUNC:
            self.match(TokenType.FUNC)
            v = self.match(TokenType.VAR)
            self.match(TokenType.LEFT_PAREN)
            p = self.P()
            self.match(TokenType.RIGHT_PAREN)
            self.match(TokenType.COLON)
            e = self.E()
            self.match(TokenType.END)
            return Func(v.val, p, e)
        elif l == TokenType.CALL:
            self.match(TokenType.CALL)
            v = self.match(TokenType.VAR)
            self.match(TokenType.LEFT_PAREN)
            a = self.A()
            self.match(TokenType.RIGHT_PAREN)
            return Call(v.val, a)
        else:
            raise ValueError

    def E(self):
        # FixMe: cleanup
        stack = []
        stack.append(self.E_helper())
        while self.lookahead() in Parser.first_BOP:
            stack.append(self.BOP())
            stack.append(self.E_helper())
        end = False
        while not end:
            prec = None
            end = True
            for i in range(len(stack)):
                s = stack[i]
                if type(s) == type and issubclass(s, BinOp):
                    if prec is not None and s.precedence <= prec:
                        e1 = stack[i-3]
                        bop = stack[i-2]
                        e2 = stack[i-1]
                        del stack[i-3: i]
                        stack.insert(i-3, bop(e1, e2))
                        end = False
                        break
                    else:
                        prec = s.precedence
        while len(stack) >= 3:
            e2 = stack.pop()
            bop = stack.pop()
            e = stack.pop()
            stack.append(bop(e, e2))
        return stack.pop()

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

    def P(self):
        l = self.lookahead()
        if l in Parser.first_P2:
            p = self.P2()
            return p
        else:
            return []

    def P2(self):
        l = self.lookahead()
        if l == TokenType.VAR:
            v = self.match(TokenType.VAR)
            p3 = self.P3()
            p3.insert(0, v.val)
            return p3
        else:
            raise ValueError

    def P3(self):
        l = self.lookahead()
        if l == TokenType.COMMA:
            self.match(TokenType.COMMA)
            return self.P2()
        else:
            return []

    def A(self):
        if self.lookahead() == TokenType.RIGHT_PAREN:  # FixMe: this is a hack
            return []
        else:
            return self.A2()

    def A2(self):
        e = self.E()
        a3 = self.A3()
        a3.insert(0, e)
        return a3

    def A3(self):
        l = self.lookahead()
        if l == TokenType.COMMA:
            self.match(TokenType.COMMA)
            return self.A2()
        else:
            return []

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
        elif l == TokenType.SUB:
            self.match(TokenType.SUB)
            return Sub
        elif l == TokenType.MUL:
            self.match(TokenType.MUL)
            return Mul
        elif l == TokenType.DIV:
            self.match(TokenType.DIV)
            return Div
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
        else:
            raise ValueError

    def parse(self):
        if self.done():
            return None
        e = self.E()
        if not self.done():
            raise ValueError
        return e

##################################################################################
# AST types
##################################################################################


class Node(object):
    def accept(self, visitor):
        pass


class BinOp(Node):
    def accept(self, visitor):
        pass


class Int(Node):
    def __init__(self, val):
        if not type(val) is int:
            raise TypeError
        self.val = val

    def accept(self, visitor):
        return visitor.visit_int(self)


class Add(BinOp):
    precedence = 5

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_add(self)


class Sub(BinOp):
    precedence = 5

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_sub(self)


class Mul(BinOp):
    precedence = 6

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_mul(self)


class Div(BinOp):
    precedence = 6

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_div(self)


class Eq(BinOp):
    precedence = 4

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_eq(self)


class NotEq(BinOp):
    precedence = 4

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_not_eq(self)


class Lt(BinOp):
    precedence = 4

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_lt(self)


class Lte(BinOp):
    precedence = 4

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_lte(self)


class Gt(BinOp):
    precedence = 4

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_gt(self)


class Gte(BinOp):
    precedence = 4

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


class And(BinOp):
    precedence = 3

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_and(self)


class Or(BinOp):
    precedence = 2

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


class Assign(BinOp):
    precedence = 1

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
        if not (len(val) > 0 and alpha(val[0]) and alphanumeric(val)):
            raise TypeError
        self.val = val

    def accept(self, visitor):
        return visitor.visit_var(self)


class Seq(BinOp):
    precedence = 0

    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_seq(self)


class Func(Node):
    def __init__(self, name, params, body):
        if not type(name) is str:
            raise TypeError
        if not type(params) is list:
            raise TypeError
        for p in params:
            if not type(p) is str:
                raise TypeError
        if not issubclass(type(body), Node):
            raise TypeError
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_func(self)


class Call(Node):
    def __init__(self, name, args):
        if not type(name) is str:
            raise TypeError
        if not type(args) is list:
            raise TypeError
        for a in args:
            if not issubclass(type(a), Node):
                raise TypeError
        self.name = name
        self.args = args

    def accept(self, visitor):
        return visitor.visit_call(self)


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

    def visit_div(self, node):
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

    def visit_func(self, node):
        raise NotImplementedError

    def visit_call(self, node):
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
        return "(%s %s %s)" % (self(node.first), TokenType.ADD.value, self(node.second))

    def visit_sub(self, node):
        if not type(node) is Sub:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.SUB.value, self(node.second))

    def visit_mul(self, node):
        if not type(node) is Mul:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.MUL.value, self(node.second))

    def visit_div(self, node):
        if not type(node) is Div:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.DIV.value, self(node.second))

    def visit_eq(self, node):
        if not type(node) is Eq:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.EQ.value, self(node.second))

    def visit_not_eq(self, node):
        if not type(node) is NotEq:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.NOT_EQ.value, self(node.second))

    def visit_lt(self, node):
        if not type(node) is Lt:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.LT.value, self(node.second))

    def visit_lte(self, node):
        if not type(node) is Lte:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.LTE.value, self(node.second))

    def visit_gt(self, node):
        if not type(node) is Gt:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.GT.value, self(node.second))

    def visit_gte(self, node):
        if not type(node) is Gte:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.GTE.value, self(node.second))

    def visit_bool(self, node):
        if not type(node) is Bool:
            raise TypeError
        return str(node.val)

    def visit_and(self, node):
        if not type(node) is And:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.AND.value, self(node.second))

    def visit_or(self, node):
        if not type(node) is Or:
            raise TypeError
        return "(%s %s %s)" % (self(node.first), TokenType.OR.value, self(node.second))

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
        return (TokenType.IF.value + TokenType.LEFT_PAREN.value + cond + TokenType.RIGHT_PAREN.value + TokenType.COLON.value +
                '\n' + indent + '  ' + tbranch + '\n' + indent +
                TokenType.ELSE.value + TokenType.COLON.value +
                '\n' + indent + '  ' + fbranch +
                '\n' + indent + TokenType.END.value)

    def visit_not(self, node):
        if not type(node) is Not:
            raise TypeError
        return '%s%s' % (TokenType.NOT.value, self(node.arg))

    def visit_while(self, node):
        if not type(node) is While:
            raise TypeError
        cond = self(node.cond)
        indent = self.indent
        self.indent = indent + "  "
        body = self(node.body)
        self.indent = indent
        return (TokenType.WHILE.value + TokenType.LEFT_PAREN.value + cond + TokenType.RIGHT_PAREN.value + TokenType.COLON.value +
                '\n' + indent + '  ' + body +
                '\n' + indent + TokenType.END.value)

    def visit_assign(self, node):
        if not type(node) is Assign:
            raise TypeError
        return "%s %s %s" % (self(node.var), TokenType.ASSIGN.value, self(node.expr))

    def visit_var(self, node):
        if not type(node) is Var:
            raise TypeError
        return node.val

    def visit_seq(self, node):
        if not type(node) is Seq:
            raise TypeError
        return "%s%s\n%s%s" % (self(node.first), TokenType.SEQ.value, self.indent, self(node.second))

    def visit_func(self, node):
        if not type(node) is Func:
            raise TypeError
        params = TokenType.LEFT_PAREN.value + \
            ",".join(node.params) + TokenType.RIGHT_PAREN.value
        indent = self.indent
        self.indent = indent + "  "
        body = self(node.body)
        self.indent = indent
        return (TokenType.FUNC.value + ' ' + node.name + params + TokenType.COLON.value +
                '\n' + indent + '  ' + body +
                '\n' + indent + TokenType.END.value)

    def visit_call(self, node):
        if not type(node) is Call:
            raise TypeError
        args = TokenType.LEFT_PAREN.value + \
            ",".join([self(a) for a in node.args]) + \
            TokenType.RIGHT_PAREN.value
        return TokenType.CALL.value + ' ' + node.name + args

##################################################################################
# AST evaluator
##################################################################################


class Evaluator(Visitor):
    def __init__(self):
        self.stack = [{}]

    def state(self):
        return self.stack[-1]

    def global_state(self):
        return self.stack[0]

    def read(self, k):
        if type(k) is not str:
            raise TypeError
        if k in self.state():
            return self.state()[k]
        return self.global_state()[k]

    def write(self, k, v):
        if type(k) is not str:
            raise TypeError
        self.state()[k] = v

    def visit_int(self, node):
        if not type(node) is Int:
            raise TypeError
        return node.val

    def visit_add(self, node):
        if not type(node) is Add:
            raise TypeError
        return self(node.first) + self(node.second)

    def visit_sub(self, node):
        if not type(node) is Sub:
            raise TypeError
        return self(node.first) - self(node.second)

    def visit_mul(self, node):
        if not type(node) is Mul:
            raise TypeError
        return self(node.first) * self(node.second)

    def visit_div(self, node):
        if not type(node) is Div:
            raise TypeError
        return self(node.first) / self(node.second)

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
        self.write(node.var.val, self(node.expr))
        return self.read(node.var.val)

    def visit_var(self, node):
        if not type(node) is Var:
            raise TypeError
        return self.read(node.val)

    def visit_seq(self, node):
        if not type(node) is Seq:
            raise TypeError
        self(node.first)
        return self(node.second)

    def visit_func(self, node):
        if not type(node) is Func:
            raise TypeError
        self.write(node.name, node)
        return False

    def visit_call(self, node):
        if not type(node) is Call:
            raise TypeError
        func = self.read(node.name)
        if not type(func) is Func:
            raise TypeError
        if len(func.params) != len(node.args):
            raise ValueError
        frame = {}
        for i, a in enumerate(node.args):
            p = func.params[i]
            frame[p] = self(a)
        self.stack.append(frame)
        out = self(func.body)
        self.stack.pop()
        return out

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="filename", help="path to SimpleLang file", type=str)
    parser.add_argument("-v", "--verbose", dest="verbose",
                        help="run in verbose mode", action='store_true')
    args = parser.parse_args()
    with open(args.filename) as f:
        src = f.read()
        print(Interpreter(src).interpret(verbose=args.verbose))
