# swimlang
#
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
# | [a-zA-Z_]+[a-zA-Z0-9_]*\{True, False, None}

##################################################################################
# Interpreter
##################################################################################

from swimlang.tokenizer import Tokenizer
from swimlang.parser import Parser
from swimlang.evaluator import Evaluator
from swimlang.printer import Printer


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
