##################################################################################
# AST evaluator
##################################################################################

# FixMe: evaluations should always result in an instance of Node, never
# a python int, str, etc. This way, we won't have to worry about
# wrapping/unwrapping in an ad hoc way.

import enum
import json
import sys
from swimlang.ast import *
from swimlang.visitor import *
from swimlang.tokenizer import QUOTE


@enum.unique
class Scope(enum.Enum):
    PARAM = enum.auto()
    LOCAL = enum.auto()
    INHERITED = enum.auto()


@enum.unique
class Decl(enum.Enum):
    LET = enum.auto()
    MUT = enum.auto()
    NONE = enum.auto()  # used for set <var> <val>


class Binding(object):
    def __init__(self, scope, decl, val):
        if type(scope) is not Scope:
            raise TypeError
        if type(decl) is not Decl:
            raise TypeError
        self.scope = scope
        self.decl = decl
        self.val = val


class Frame(object):
    def __init__(self, fun, env):
        if not (type(fun) is Fun or fun is None):
            raise TypeError
        if not type(env) is dict:
            raise TypeError
        self.fun = fun
        self.env = env


class Evaluator(Visitor):
    def __init__(self):
        self.stack = [Frame(None, {})]

    def current_frame(self):
        return self.stack[-1]

    def read(self, name, frame=None):
        if type(name) is not str:
            raise TypeError
        frame = self.current_frame() if frame is None else frame
        if name in frame.env:
            return frame.env[name]
        return None

    def write(self, name, binding, frame=None):
        if type(name) is not str:
            raise TypeError
        frame = self.current_frame() if frame is None else frame
        current_binding = frame.env.get(name, None)
        if current_binding is None:
            frame.env[name] = binding
        elif current_binding.scope == Scope.LOCAL:
            if binding.decl in [Decl.LET, Decl.MUT]:
                raise ValueError(
                    "re-declaration of %s inside local scope" % name)
            elif current_binding.decl == Decl.LET:
                raise ValueError("cannot rebind non-mutable %s" % name)
            else:
                frame.env[name] = binding
        elif current_binding.scope == Scope.INHERITED:
            if binding.decl in [Decl.LET, Decl.MUT]:
                frame.env[name] = binding
            elif current_binding.decl == Decl.LET:
                raise ValueError("cannot rebind non-mutable %s" % name)
            else:
                frame.env[name] = binding
        elif current_binding.scope == Scope.PARAM:
            if binding.decl in [Decl.LET, Decl.MUT]:
                raise ValueError("re-declaration of param %s" % name)
            elif current_binding.decl == Decl.LET:
                raise ValueError("cannot rebind non-mutable %s" % name)
            else:
                raise AssertionError("found mutable param %s" % name)
        else:
            raise AssertionError("unknown scope type %s" %
                                 str(current_binding.scope))

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
        return int(self(node.first) / self(node.second))

    def visit_mod(self, node):
        if not type(node) is Mod:
            raise TypeError
        return self(node.first) % self(node.second)

    def visit_eq(self, node):
        if not type(node) is Eq:
            raise TypeError
        return self(node.first) == self(node.second)

    def visit_exit(self, node):
        if not type(node) is Exit:
            raise TypeError
        sys.exit(0)

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

    def visit_str(self, node):
        if not type(node) is Str:
            raise TypeError
        return json.loads('%s%s%s' % (QUOTE, node.val, QUOTE))

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

    def visit_let(self, node):
        if not type(node) is Let:
            raise TypeError
        val = self(node.expr)
        binding = Binding(Scope.LOCAL, Decl.LET, val)
        self.write(node.var.val, binding)
        return val

    def visit_mut(self, node):
        if not type(node) is Mut:
            raise TypeError
        val = self(node.expr)
        binding = Binding(Scope.LOCAL, Decl.MUT, val)
        self.write(node.var.val, binding)
        return val

    def visit_set(self, node):
        if not type(node) is Set:
            raise TypeError
        binding = self.read(node.var.val)
        if binding is None:
            raise ValueError
        val = self(node.expr)
        binding = Binding(binding.scope, Decl.NONE, val)
        self.write(node.var.val, binding)
        # Propagate write up call stack as long as the calling context is the same as the lexical
        # scope, as is the case when nested functions are called within their enclosing lexical
        # scope. Note that the lexical scope can be different from the calling context, e.g.
        # when a nested function is returned and subsequently called outside of its lexical scope;
        # in this case, no propagation is necessary.
        fun = self.current_frame().fun
        idx = -2  # index for previous stack frame
        while binding.scope == Scope.INHERITED and fun and fun.lexical_scope == self.stack[idx].fun:
            binding = self.read(node.var.val, self.stack[idx])
            binding.val = val
            fun = fun.lexical_scope
            idx -= 1
        return val

    def visit_var(self, node):
        if not type(node) is Var:
            raise TypeError
        binding = self.read(node.val)
        if binding is None:
            raise ValueError
        return binding.val

    def visit_seq(self, node):
        if not type(node) is Seq:
            raise TypeError
        self(node.first)
        return self(node.second)

    def visit_fun(self, node):
        if not type(node) is Fun:
            raise TypeError

        # Function is anonymous, i.e. a closure. Just return it.
        if node.name is None:
            return node

        # Function delcaration case.
        # Make an anonymous copy of the function which will be returned.
        # This is important to prevent re-declarations and to support closures.
        out = Fun(None, node.params, node.body, self.current_frame().fun)
        out.env = {}
        for name, binding in self.current_frame().env.items():
            out.env[name] = Binding(Scope.INHERITED, binding.decl, binding.val)
        out.env[node.name] = Binding(Scope.PARAM, Decl.LET, out)
        self.write(node.name, Binding(Scope.LOCAL, Decl.LET, out))
        return out

    def visit_call(self, node):
        if not type(node) is Call:
            raise TypeError
        fun = self(node.fun)
        if not type(fun) is Fun:
            # Non-functions are callable in that they take no arguments and return themselves.
            if len(node.args) == 0:
                return fun
            # Non-functions cannot take arguments.
            raise TypeError
        if len(fun.params) < len(node.args):
            # Too many arguments supplied
            raise ValueError
        if len(fun.params) == len(node.args):
            # All params available - evaluate the function
            env = {}
            for name, binding in fun.env.items():
                env[name] = Binding(binding.scope, binding.decl, binding.val)
            for i, a in enumerate(node.args):
                name = fun.params[i]
                env[name] = Binding(Scope.PARAM, Decl.LET, self(a))
            self.stack.append(Frame(fun, env))
            out = self(fun.body)
            self.stack.pop()
        else:
            # Not all params available - return a closure
            params = [p for p in fun.params[len(node.args):]]
            out = Fun(None, params, fun.body, fun.lexical_scope)
            for name, binding in fun.env.items():
                out.env[name] = Binding(
                    binding.scope, binding.decl, binding.val)
            for i, a in enumerate(node.args):
                name = fun.params[i]
                out.env[name] = Binding(Scope.PARAM, Decl.LET, self(a))
        return out

    def visit_map(self, node):
        if not type(node) is Map:
            raise TypeError
        mappings = {}
        for k, v in node.mappings.items():
            mappings[Node.wrap(self(k))] = Node.wrap(self(v))
        return Map(mappings)

    def visit_get(self, node):
        if not type(node) is Get:
            raise TypeError
        m = self(node.m)
        if not type(m) is Map:
            raise TypeError
        k = Node.wrap(self(node.k))
        if k not in m.mappings:
            raise KeyError
        v = m.mappings[k]
        return self(v)

    def visit_put(self, node):
        if not type(node) is Put:
            raise TypeError
        m = self(node.m)
        if not type(m) is Map:
            raise TypeError
        k = Node.wrap(self(node.k))
        v = Node.wrap(self(node.v))
        new_mappings = m.mappings.put(k, v)
        return Map(new_mappings)

    def visit_keys(self, node):
        if not type(node) is Keys:
            raise TypeError
        m = self(node.m)
        if not type(m) is Map:
            raise TypeError
        keys = List(m.mappings.keys())
        return keys

    def visit_list(self, node):
        if not type(node) is List:
            raise TypeError
        return List([Node.wrap(self(e)) for e in node.elements])

    def visit_head(self, node):
        if not type(node) is Head:
            raise TypeError
        l = self(node.arg)
        if type(l) is List:
            if len(l.elements) <= 0:
                raise ValueError
            head = l.elements.head()
            return self(head)
        if type(l) is str:
            if len(l) <= 0:
                raise ValueError
            else:
                return l[0]
        raise TypeError

    def visit_tail(self, node):
        if not type(node) is Tail:
            raise TypeError
        l = self(node.arg)
        if type(l) is List:
            if len(l.elements) <= 0:
                raise ValueError
            tail = l.elements.tail()
            return List(tail)
        if type(l) is str:
            if len(l) <= 0:
                raise ValueError
            else:
                return l[1:]
        raise TypeError

    def visit_push(self, node):
        if not type(node) is Push:
            raise TypeError
        l = self(node.tail)
        if not type(l) is List:
            raise TypeError
        tail = l.elements
        head = Node.wrap(self(node.head))
        return List(tail.push(head))

    def visit_print(self, node):
        if not type(node) is Print:
            raise TypeError
        print(self(node.arg))
        return Nil.instance()

    def visit_type(self, node):
        if not type(node) is Type:
            raise TypeError
        return type(Node.wrap(self(node.arg)))

    def visit_nil(self, node):
        if not type(node) is Nil:
            raise TypeError
        return node
