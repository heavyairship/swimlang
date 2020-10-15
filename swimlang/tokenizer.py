##################################################################################
# Tokenizer
##################################################################################

import enum
from swimlang.util import *

QUOTE = '"'
COMMENT = "#"


@enum.unique
class TokenType(enum.Enum):
    WHILE = "while"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COLON = ":"
    IF = "if"
    FUN = "fun"
    LET = "let"
    MUT = "mut"
    SET = "set"
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
    MOD = "%"
    SEQ = ";"
    HEAD = "head"
    TAIL = "tail"
    PUSH = "push"
    GET = "get"
    PUT = "put"
    KEYS = "keys"
    TYPE = "type"
    PRINT = "print"
    TRUE = "True"
    FALSE = "False"
    NIL = "Nil"
    INT = enum.auto()
    VAR = enum.auto()
    STR = enum.auto()


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
    TokenType.FUN.value,
    TokenType.LET.value,
    TokenType.MUT.value,
    TokenType.SET.value,
    TokenType.TRUE.value,
    TokenType.FALSE.value,
    TokenType.NIL.value,
    TokenType.HEAD.value,
    TokenType.TAIL.value,
    TokenType.PUSH.value,
    TokenType.GET.value,
    TokenType.PUT.value,
    TokenType.KEYS.value,
    TokenType.PRINT.value,
    TokenType.TYPE.value
]


class Tokenizer(object):
    def __init__(self, src):
        self.src = self.remove_comments(src)
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
            after_kw = self.at(self.idx+n)
            if self.peek(n) == kw and not (alphanumeric(after_kw) or after_kw == '_'):
                self.match(kw)
                self.emit(TokenType(kw))
                return True
        return False

    def match_int(self):
        old_idx = self.idx
        sign = 1
        while self.peek() == '-':
            self.next()
            sign *= -1
        num = ""
        while numeric(self.peek()):
            num += self.next()
        if alpha(self.peek()) or num == "":
            self.idx = old_idx
            return False
        val = sign*int(num)
        self.emit(TokenType.INT, val)
        return True

    def match_str(self):
        if not self.match(QUOTE):
            return False
        val = ""
        while self.peek() and self.peek().isascii():
            prev_is_not_escape = len(val) == 0 or val[-1] is not '\\'
            prev_is_double_escape = len(val) >= 2 and val[-2:] == "\\\\"
            if self.peek() == QUOTE and (prev_is_not_escape or prev_is_double_escape):
                break
            val += self.next()
        if not self.match(QUOTE):
            raise ValueError
        self.emit(TokenType.STR, val)
        return True

    def match_var(self):
        if not valid_var(self.peek()):
            return False
        var = ""
        while alphanumeric(self.peek()) or self.peek() == '_':
            var += self.next()
        self.emit(TokenType.VAR, var)
        return True

    def match_space(self):
        found_space = False
        while isspace(self.peek()):
            self.next()
            found_space = True
        return found_space

    def remove_comments(self, src):
        out = []
        for line in src.split('\n'):
            found_comment = False
            in_quotes = False
            for idx, char in enumerate(line):
                if not in_quotes and char == QUOTE:
                    in_quotes = True
                elif in_quotes and char == QUOTE and line[idx-1] != '\\':
                    in_quotes = False
                if char == COMMENT and not in_quotes:
                    out.append(line[:idx])
                    found_comment = True
                    break
            if not found_comment:
                out.append(line)
        return '\n'.join(out)

    def tokenize(self):
        if self.done():
            return []
        while not self.done():
            if self.match(TokenType.NOT_EQ.value):
                self.emit(TokenType.NOT_EQ)
            elif self.match(TokenType.LTE.value):
                self.emit(TokenType.LTE)
            elif self.match(TokenType.GTE.value):
                self.emit(TokenType.GTE)
            elif self.match(TokenType.LEFT_PAREN.value):
                self.emit(TokenType.LEFT_PAREN)
            elif self.match(TokenType.RIGHT_PAREN.value):
                self.emit(TokenType.RIGHT_PAREN)
            elif self.match(TokenType.LEFT_BRACKET.value):
                self.emit(TokenType.LEFT_BRACKET)
            elif self.match(TokenType.RIGHT_BRACKET.value):
                self.emit(TokenType.RIGHT_BRACKET)
            elif self.match(TokenType.LEFT_BRACE.value):
                self.emit(TokenType.LEFT_BRACE)
            elif self.match(TokenType.RIGHT_BRACE.value):
                self.emit(TokenType.RIGHT_BRACE)
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
            elif self.match_int():
                pass
            elif self.match(TokenType.SUB.value):
                self.emit(TokenType.SUB)
            elif self.match(TokenType.MUL.value):
                self.emit(TokenType.MUL)
            elif self.match(TokenType.DIV.value):
                self.emit(TokenType.DIV)
            elif self.match(TokenType.MOD.value):
                self.emit(TokenType.MOD)
            elif self.match(TokenType.SEQ.value):
                self.emit(TokenType.SEQ)
            elif self.match_keyword():
                pass
            elif self.match_var():
                pass
            elif self.match_str():
                pass
            elif self.match_space():
                pass
            else:
                raise ValueError
        return self.tokens
