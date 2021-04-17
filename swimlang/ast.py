##################################################################################
# AST types
##################################################################################

from swimlang.util import valid_var
from swimlang.pdstruct import *
from swimlang.tokenizer import TokenType


class Node(object):
    @staticmethod
    def wrap(e):
        if type(e) is int:
            return Int(e)
        elif type(e) is bool:
            return Bool(e)
        elif type(e) is str:
            return Str(e)
        else:
            return e

    @staticmethod
    def unwrap(e):
        if type(e) in [Int, Bool, Str]:
            return e.val
        else:
            return e

    def accept(self, visitor):
        pass

class UOp(Node):
    def accept(self, visitor):
        pass

class Exit(UOp):
    def accept(self, visitor):
        return visitor.visit_exit(self)

class BinOp(Node):
    def accept(self, visitor):
        pass


class Int(Node):
    def __init__(self, val):
        if not type(val) is int:
            raise TypeError
        self.val = val

    def __hash__(self):
        return self.val.__hash__()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.val == other.val

    def accept(self, visitor):
        return visitor.visit_int(self)


class Add(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_add(self)


class Sub(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_sub(self)


class Mul(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_mul(self)


class Div(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_div(self)


class Mod(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_mod(self)


class Eq(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_eq(self)


class NotEq(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_not_eq(self)


class Lt(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_lt(self)


class Lte(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_lte(self)


class Gt(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_gt(self)


class Gte(BinOp):
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

    def __hash__(self):
        return self.val.__hash__()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.val == other.val

    def accept(self, visitor):
        return visitor.visit_bool(self)


class And(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_and(self)


class Or(BinOp):
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


class Str(Node):
    def __init__(self, val):
        if not type(val) is str:
            raise TypeError
        self.val = val

    def __hash__(self):
        return self.val.__hash__()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.val == other.val

    def accept(self, visitor):
        return visitor.visit_str(self)


class If(Node):
    def __init__(self, cond, first, second):
        if not (issubclass(type(cond), Node) and issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.cond = cond
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_if(self)


class While(BinOp):
    def __init__(self, cond, body):
        if not (issubclass(type(cond), Node) and issubclass(type(body), Node)):
            raise TypeError
        self.cond = cond
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while(self)


class Let(Node):
    def __init__(self, var, expr):
        if not type(var) is Var:
            raise TypeError
        if not issubclass(type(expr), Node):
            raise TypeError
        self.var = var
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_let(self)


class Mut(Node):
    def __init__(self, var, expr):
        if not type(var) is Var:
            raise TypeError
        if not issubclass(type(expr), Node):
            raise TypeError
        self.var = var
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_mut(self)


class Set(Node):
    def __init__(self, var, expr):
        if not type(var) is Var:
            raise TypeError
        if not issubclass(type(expr), Node):
            raise TypeError
        self.var = var
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_set(self)


class Var(Node):
    def __init__(self, val):
        if not type(val) is str:
            raise TypeError
        if not valid_var(val):
            raise TypeError
        self.val = val

    def accept(self, visitor):
        return visitor.visit_var(self)


class Seq(BinOp):
    def __init__(self, first, second):
        if not (issubclass(type(first), Node) and issubclass(type(second), Node)):
            raise TypeError
        self.first = first
        self.second = second

    def accept(self, visitor):
        return visitor.visit_seq(self)


class Fun(Node):
    def __init__(self, name, params, body, lexical_scope):
        if not (type(name) is str or name is None):
            raise TypeError
        if not type(params) is list:
            raise TypeError
        for p in params:
            if not type(p) is str:
                raise TypeError
            if p == name:
                raise ValueError
        if not issubclass(type(body), Node):
            raise TypeError
        if not (type(lexical_scope) is Fun or lexical_scope is None):
            raise TypeError
        self.name = name
        self.params = params
        self.body = body
        self.env = {}
        self.lexical_scope = lexical_scope

    def accept(self, visitor):
        return visitor.visit_fun(self)


class Call(Node):
    def __init__(self, fun, args):
        if not issubclass(type(fun), Node):
            raise TypeError
        if not type(args) is list:
            raise TypeError
        for a in args:
            if not issubclass(type(a), Node):
                raise TypeError
        self.fun = fun
        self.args = args

    def accept(self, visitor):
        return visitor.visit_call(self)


class Map(Node):
    # FixMe: don't expose P_Tree internals?
    def __init__(self, mappings):
        if type(mappings) is dict:
            for k, v in mappings.items():
                if not (issubclass(type(k), Node) and issubclass(type(v), Node)):
                    raise TypeError
            self.mappings = P_Tree(init_mappings=mappings)
        elif type(mappings) is P_Tree:
            self.mappings = mappings
        else:
            raise TypeError

    def accept(self, visitor):
        return visitor.visit_map(self)

    def __str__(self):
        from swimlang.printer import Printer
        return Printer()(self)

    def __bool__(self):
        return len(self.mappings) != 0


class Get(Node):
    def __init__(self, m, k):
        if not (issubclass(type(m), Node) and issubclass(type(k), Node)):
            raise TypeError
        self.m = m
        self.k = k

    def accept(self, visitor):
        return visitor.visit_get(self)


class Put(Node):
    def __init__(self, m, k, v):
        if not (issubclass(type(m), Node) and issubclass(type(k), Node) and issubclass(type(v), Node)):
            raise TypeError
        self.m = m
        self.k = k
        self.v = v

    def accept(self, visitor):
        return visitor.visit_put(self)


class Keys(Node):
    def __init__(self, m):
        if not issubclass(type(m), Node):
            raise TypeError
        self.m = m

    def accept(self, visitor):
        return visitor.visit_keys(self)


class Type(Node):
    def __init__(self, arg):
        if not issubclass(type(arg), Node):
            raise TypeError
        self.arg = arg

    def accept(self, visitor):
        return visitor.visit_type(self)


class List(Node):
    # FixMe: don't expose P_List internals?
    def __init__(self, elements):
        if type(elements) is list:
            for e in elements:
                if not issubclass(type(e), Node):
                    raise TypeError
            self.elements = P_List(initial=elements)
        elif type(elements) is P_List:
            self.elements = elements
        else:
            raise TypeError

    def accept(self, visitor):
        return visitor.visit_list(self)

    def __str__(self):
        from swimlang.printer import Printer
        return Printer()(self)

    def __bool__(self):
        return len(self.elements) != 0


class Head(Node):
    def __init__(self, arg):
        if not issubclass(type(arg), Node):
            raise TypeError
        self.arg = arg

    def accept(self, visitor):
        return visitor.visit_head(self)


class Tail(Node):
    def __init__(self, arg):
        if not issubclass(type(arg), Node):
            raise TypeError
        self.arg = arg

    def accept(self, visitor):
        return visitor.visit_tail(self)


class Push(BinOp):
    def __init__(self, head, tail):
        if not (issubclass(type(head), Node) and issubclass(type(tail), Node)):
            raise TypeError
        self.head = head
        self.tail = tail

    def accept(self, visitor):
        return visitor.visit_push(self)


class Print(Node):
    def __init__(self, arg):
        if not issubclass(type(arg), Node):
            raise TypeError
        self.arg = arg

    def accept(self, visitor):
        return visitor.visit_print(self)


class Nil(Node):
    __instance__ = None

    @staticmethod
    def instance():
        if Nil.__instance__ is None:
            return Nil()
        return Nil.__instance__

    def __init__(self):
        if Nil.__instance__ is None:
            Nil.__instance__ = self
        else:
            raise Exception("")

    def __str__(self):
        return TokenType.NIL.value

    def __hash__(self):
        return None.__hash__()

    def __bool__(self):
        return False

    def accept(self, visitor):
        return visitor.visit_nil(self)
