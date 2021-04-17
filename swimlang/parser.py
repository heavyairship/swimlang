##################################################################################
# Parser/AST generator
##################################################################################

# FixMe: make evaluation iterative not recursive to avoid max recursion depth errors
# FixMe: add tail recursion
# FixMe: add messages for parse/eval errors
# FixMe: should if/while create their own lexical scopes?
# FixMe: always re-wrap primitives (e.g. int -> Int)?
# FixMe: add len keyword
# FixMe: fix issue where each closure gets a copy of its mutable environment
# FixMe: make most of the keyword operators built-in functions rather than syntax
# FixMe: add in keyword
# FixMe: add arrays?
#
# Comments start with # and extend until the end of line.
#
# Grammar:
#
# E -> (expression)
# | T
# | (fun v P: E)
# | (E L)
# | (let v E)
# | (mut v E)
# | (set v E)
# | (NOP)
# | (UOP E)
# | (BOP E E)
# | (TOP E E E)
# | E;E1
#
# E1 -> (expression helper)
# | ε
# | E
#
# T -> (term)
# | n
# | b
# | s
# | v
# | [L]
# | {M}
# | Nil
#
# M -> (mapping)
# | ε
# | E:E M
#
# P -> (parameter list)
# | ε
# | v P
#
# L -> (expression list)
# | ε
# | E L
#
# NOP -> (nullary operator)
# | exit
#
# UOP -> (unary operator)
# | !
# | head
# | tail
# | print
# | keys
# | type
#
# BOP -> (binary operator)
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
# | %
# | while
# | push
# | get
#
# TOP -> (ternary operator)
# | if
# | put
#
# b -> (boolean atom)
# | True
# | False
#
# n -> (integer atom)
# | [-]*[0-9]+
#
# s -> (string atom) # double quotes surrounding any ascii character
# | "[\x00-\x7F]+"
#
# v -> (variable) # FixMe: var/id should be different
# | [a-zA-Z_]+[a-zA-Z0-9_]*\{True, False, Nil}

from swimlang.tokenizer import TokenType
from swimlang.ast import *


class Parser(object):
    first_b = frozenset([TokenType.TRUE, TokenType.FALSE])

    first_T = frozenset([TokenType.INT, TokenType.VAR, TokenType.STR,
                         TokenType.LEFT_BRACKET, TokenType.LEFT_BRACE, TokenType.NIL]).union(first_b)

    first_NOP = frozenset([TokenType.EXIT])
    
    first_UOP = frozenset([TokenType.NOT, TokenType.HEAD,
                           TokenType.TAIL, TokenType.KEYS, TokenType.PRINT, TokenType.TYPE])

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
        TokenType.MOD,
        TokenType.SEQ,
        TokenType.WHILE,
        TokenType.PUSH,
        TokenType.GET])

    first_TOP = frozenset([TokenType.IF, TokenType.PUT])

    first_E = frozenset([TokenType.LEFT_PAREN]).union(first_T)

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

    def E(self):
        l = self.lookahead()
        if l in self.first_T:
            e = self.T()
        elif l == TokenType.LEFT_PAREN:
            self.match(TokenType.LEFT_PAREN)
            l2 = self.lookahead()
            if l2 == TokenType.FUN:
                self.match(TokenType.FUN)
                v = self.v()
                p = self.P()
                self.match(TokenType.COLON)
                e = self.E()
                self.match(TokenType.RIGHT_PAREN)
                e = Fun(v.val, p, e, None)
            elif l2 == TokenType.LET:
                self.match(TokenType.LET)
                v = self.v()
                e = self.E()
                self.match(TokenType.RIGHT_PAREN)
                e = Let(v, e)
            elif l2 == TokenType.MUT:
                self.match(TokenType.MUT)
                v = self.v()
                e = self.E()
                self.match(TokenType.RIGHT_PAREN)
                e = Mut(v, e)
            elif l2 == TokenType.SET:
                self.match(TokenType.SET)
                v = self.v()
                e = self.E()
                self.match(TokenType.RIGHT_PAREN)
                e = Set(v, e)
            elif l2 in self.first_NOP:
                nop = self.NOP()
                self.match(TokenType.RIGHT_PAREN)
                e = nop()
            elif l2 in self.first_UOP:
                uop = self.UOP()
                e = self.E()
                self.match(TokenType.RIGHT_PAREN)
                e = uop(e)
            elif l2 in self.first_BOP:
                bop = self.BOP()
                e = self.E()
                e2 = self.E()
                self.match(TokenType.RIGHT_PAREN)
                e = bop(e, e2)
            elif l2 in self.first_TOP:
                top = self.TOP()
                e = self.E()
                e2 = self.E()
                e3 = self.E()
                self.match(TokenType.RIGHT_PAREN)
                e = top(e, e2, e3)
            elif l2 in self.first_E:
                e = self.E()
                lst = self.L()
                self.match(TokenType.RIGHT_PAREN)
                e = Call(e, lst)
            else:
                raise ValueError
        else:
            raise ValueError
        matched_seq = (self.lookahead() == TokenType.SEQ)
        while self.lookahead() == TokenType.SEQ:
            self.match(TokenType.SEQ)
        e1 = self.E1() if matched_seq else None
        return e if e1 is None else Seq(e, e1)

    def E1(self):
        l = self.lookahead()
        if l in self.first_E:
            e = self.E()
            return e
        else:
            return None

    def T(self):
        l = self.lookahead()
        if l == TokenType.INT:
            n = self.match(TokenType.INT)
            return Int(n.val)
        elif l in Parser.first_b:
            b = self.b()
            return Bool(b)
        elif l == TokenType.VAR:
            v = self.v()
            return v
        elif l == TokenType.LEFT_BRACKET:
            self.match(TokenType.LEFT_BRACKET)
            lst = self.L()
            self.match(TokenType.RIGHT_BRACKET)
            return List(lst)
        elif l == TokenType.LEFT_BRACE:
            self.match(TokenType.LEFT_BRACE)
            m = self.M()
            self.match(TokenType.RIGHT_BRACE)
            return Map(m)
        elif l == TokenType.STR:
            s = self.match(TokenType.STR)
            return Str(s.val)
        elif l == TokenType.NIL:
            self.match(TokenType.NIL)
            return Nil.instance()
        else:
            raise ValueError

    def M(self):
        l = self.lookahead()
        if l in self.first_E:
            k = self.E()
            self.match(TokenType.COLON)
            v = self.E()
            m = self.M()
            m[k] = v
            return m
        else:
            return {}

    def P(self):
        l = self.lookahead()
        if l == TokenType.VAR:
            v = self.v().val
            p = self.P()
            p.insert(0, v)
            return p
        else:
            return []

    def L(self):
        l = self.lookahead()
        if l in self.first_E:
            e = self.E()
            lst = self.L()
            lst.insert(0, e)
            return lst
        else:
            return []

    def NOP(self):
        l = self.lookahead()
        if l == TokenType.EXIT:
            self.match(TokenType.EXIT)
            return Exit
        else:
            raise ValueError

    def UOP(self):
        l = self.lookahead()
        if l == TokenType.NOT:
            self.match(TokenType.NOT)
            return Not
        elif l == TokenType.HEAD:
            self.match(TokenType.HEAD)
            return Head
        elif l == TokenType.TAIL:
            self.match(TokenType.TAIL)
            return Tail
        elif l == TokenType.PRINT:
            self.match(TokenType.PRINT)
            return Print
        elif l == TokenType.KEYS:
            self.match(TokenType.KEYS)
            return Keys
        elif l == TokenType.TYPE:
            self.match(TokenType.TYPE)
            return Type
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
        elif l == TokenType.MOD:
            self.match(TokenType.MOD)
            return Mod
        elif l == TokenType.WHILE:
            self.match(TokenType.WHILE)
            return While
        elif l == TokenType.PUSH:
            self.match(TokenType.PUSH)
            return Push
        elif l == TokenType.GET:
            self.match(TokenType.GET)
            return Get
        else:
            raise ValueError

    def TOP(self):
        l = self.lookahead()
        if l == TokenType.IF:
            self.match(TokenType.IF)
            return If
        elif l == TokenType.PUT:
            self.match(TokenType.PUT)
            return Put
        else:
            raise ValueError

    def v(self):
        l = self.lookahead()
        if l == TokenType.VAR:
            v = self.match(TokenType.VAR)
            return Var(v.val)
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
            raise ValueError("empty file")
        e = self.E()
        if not self.done():
            raise ValueError
        return e
