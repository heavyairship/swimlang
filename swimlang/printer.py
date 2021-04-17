##################################################################################
# AST printer
##################################################################################

from swimlang.ast import *
from swimlang.visitor import *
from swimlang.tokenizer import TokenType
from swimlang.tokenizer import QUOTE


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
        return "(%s %s %s)" % (TokenType.ADD.value, self(node.first), self(node.second))

    def visit_sub(self, node):
        if not type(node) is Sub:
            raise TypeError
        return "(%s %s %s)" % (TokenType.SUB.value, self(node.first), self(node.second))

    def visit_mul(self, node):
        if not type(node) is Mul:
            raise TypeError
        return "(%s %s %s)" % (TokenType.MUL.value, self(node.first), self(node.second))

    def visit_div(self, node):
        if not type(node) is Div:
            raise TypeError
        return "(%s %s %s)" % (TokenType.DIV.value, self(node.first), self(node.second))

    def visit_mod(self, node):
        if not type(node) is Mod:
            raise TypeError
        return "(%s %s %s)" % (TokenType.MOD.value, self(node.first), self(node.second))

    def visit_eq(self, node):
        if not type(node) is Eq:
            raise TypeError
        return "(%s %s %s)" % (TokenType.EQ.value, self(node.first), self(node.second))

    def visit_not_eq(self, node):
        if not type(node) is NotEq:
            raise TypeError
        return "(%s %s %s)" % (TokenType.NOT_EQ.value, self(node.first), self(node.second))

    def visit_lt(self, node):
        if not type(node) is Lt:
            raise TypeError
        return "(%s %s %s)" % (TokenType.LT.value, self(node.first), self(node.second))

    def visit_lte(self, node):
        if not type(node) is Lte:
            raise TypeError
        return "(%s %s %s)" % (TokenType.LTE.value, self(node.first), self(node.second))

    def visit_gt(self, node):
        if not type(node) is Gt:
            raise TypeError
        return "(%s %s %s)" % (TokenType.GT.value, self(node.first), self(node.second))

    def visit_gte(self, node):
        if not type(node) is Gte:
            raise TypeError
        return "(%s %s %s)" % (TokenType.GTE.value, self(node.first), self(node.second))

    def visit_bool(self, node):
        if not type(node) is Bool:
            raise TypeError
        return str(node.val)

    def visit_and(self, node):
        if not type(node) is And:
            raise TypeError
        return "(%s %s %s)" % (TokenType.AND.value, self(node.first), self(node.second))

    def visit_or(self, node):
        if not type(node) is Or:
            raise TypeError
        return "(%s %s %s)" % (TokenType.OR.value, self(node.first), self(node.second))

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
        return (TokenType.LEFT_PAREN.value + TokenType.IF.value + ' ' + cond +
                '\n' + indent + '  ' + tbranch +
                '\n' + indent + '  ' + fbranch +
                '\n' + indent + TokenType.RIGHT_PAREN.value)

    def visit_exit(self, node):
        if not type(node) is Exit:
            raise TypeError
        return TokenType.LEFT_PAREN.value + TokenType.EXIT.value + TokenType.RIGHT_PAREN.value
        
    def visit_not(self, node):
        if not type(node) is Not:
            raise TypeError
        return TokenType.LEFT_PAREN.value + TokenType.NOT.value + self(node.arg) + TokenType.RIGHT_PAREN.value

    def visit_str(self, node):
        if not type(node) is Str:
            raise TypeError
        return "%s%s%s" % (QUOTE, node.val, QUOTE)

    def visit_while(self, node):
        if not type(node) is While:
            raise TypeError
        cond = self(node.cond)
        indent = self.indent
        self.indent = indent + "  "
        body = self(node.body)
        self.indent = indent
        return (TokenType.LEFT_PAREN.value + TokenType.WHILE.value + " " + cond +
                '\n' + indent + '  ' + body +
                '\n' + indent + TokenType.RIGHT_PAREN.value)

    def visit_let(self, node):
        if not type(node) is Let:
            raise TypeError
        return "(%s %s %s)" % (TokenType.LET.value, self(node.var), self(node.expr))

    def visit_mut(self, node):
        if not type(node) is Mut:
            raise TypeError
        return "(%s %s %s)" % (TokenType.MUT.value, self(node.var), self(node.expr))

    def visit_set(self, node):
        if not type(node) is Set:
            raise TypeError
        return "(%s %s %s)" % (TokenType.SET.value, self(node.var), self(node.expr))

    def visit_var(self, node):
        if not type(node) is Var:
            raise TypeError
        return node.val

    def visit_seq(self, node):
        if not type(node) is Seq:
            raise TypeError
        return "%s%s\n%s%s" % (self(node.first), TokenType.SEQ.value, self.indent, self(node.second))

    def visit_fun(self, node):
        if not type(node) is Fun:
            raise TypeError
        if node.name:
            fun_name = node.name
        else:
            # FixMe: this prob should be removed b/c List/Map __str__ functions should not use Printer
            # Hack to look up names for 'anonymous' functions
            fun_name = [n for (n, b) in node.env.items() if b.val == node][0]
        params = " " + " ".join(node.params) if len(node.params) > 0 else ""
        indent = self.indent
        self.indent = indent + "  "
        body = self(node.body)
        self.indent = indent
        return (TokenType.LEFT_PAREN.value + TokenType.FUN.value + ' ' + fun_name + params + TokenType.COLON.value +
                '\n' + indent + '  ' + body +
                '\n' + indent + TokenType.RIGHT_PAREN.value)

    def visit_call(self, node):
        if not type(node) is Call:
            raise TypeError
        args = " " + " ".join([self(a) for a in node.args]
                              ) if len(node.args) > 0 else ""
        return (TokenType.LEFT_PAREN.value + self(node.fun) + args +
                TokenType.RIGHT_PAREN.value)

    def visit_map(self, node):
        if not type(node) is Map:
            raise TypeError
        if len(node.mappings) == 0:
            return TokenType.LEFT_BRACE.value + TokenType.RIGHT_BRACE.value
        indent = self.indent
        self.indent = indent + "  "
        mappings = ("\n" + self.indent).join(
            [("%s%s%s" % (self(k), TokenType.COLON.value, self(node.mappings[k]))) for k in node.mappings])
        self.indent = indent
        return TokenType.LEFT_BRACE.value + "\n" + self.indent + "  " + mappings + "\n" + self.indent + TokenType.RIGHT_BRACE.value

    def visit_get(self, node):
        if not type(node) is Get:
            raise TypeError
        return (TokenType.LEFT_PAREN.value + TokenType.GET.value + " " + self(node.m) + " " + self(node.k) +
                TokenType.RIGHT_PAREN.value)

    def visit_put(self, node):
        if not type(node) is Put:
            raise TypeError
        return (TokenType.LEFT_PAREN.value + TokenType.PUT.value + " " + self(node.m) + " " + self(node.k) + " " +
                self(node.v) + TokenType.RIGHT_PAREN.value)

    def visit_keys(self, node):
        if not type(node) is Keys:
            raise TypeError
        return (TokenType.LEFT_PAREN.value + TokenType.KEYS.value + " " + self(node.m) + TokenType.RIGHT_PAREN.value)

    def visit_type(self, node):
        if not type(node) is Type:
            raise TypeError
        return (TokenType.LEFT_PAREN.value + TokenType.TYPE.value + " " + self(node.arg) + TokenType.RIGHT_PAREN.value)

    def visit_list(self, node):
        if not type(node) is List:
            raise TypeError
        elements = " ".join([self(e) for e in node.elements]) if len(
            node.elements) > 0 else ""
        return TokenType.LEFT_BRACKET.value + elements + TokenType.RIGHT_BRACKET.value

    def visit_head(self, node):
        if not type(node) is Head:
            raise TypeError
        return (TokenType.LEFT_PAREN.value + TokenType.HEAD.value + " " + self(node.arg) +
                TokenType.RIGHT_PAREN.value)

    def visit_tail(self, node):
        if not type(node) is Tail:
            raise TypeError
        return (TokenType.LEFT_PAREN.value + TokenType.TAIL.value + " " + self(node.arg) +
                TokenType.RIGHT_PAREN.value)

    def visit_push(self, node):
        if not type(node) is Push:
            raise TypeError
        return (TokenType.LEFT_PAREN.value + TokenType.PUSH.value + " " + self(node.head) + " " +
                self(node.tail) + TokenType.RIGHT_PAREN.value)

    def visit_print(self, node):
        if not type(node) is Print:
            raise TypeError
        return (TokenType.LEFT_PAREN.value + TokenType.PRINT.value + " " + self(node.arg) +
                TokenType.RIGHT_PAREN.value)

    def visit_nil(self, node):
        if not type(node) is Nil:
            raise TypeError
        return TokenType.NIL.value
