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

    def visit_mod(self, node):
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

    def visit_str(self, node):
        raise NotImplementedError

    def visit_while(self, node):
        raise NotImplementedError

    def visit_let(self, node):
        raise NotImplementedError

    def visit_mut(self, node):
        raise NotImplementedError

    def visit_var(self, node):
        raise NotImplementedError

    def visit_seq(self, node):
        raise NotImplementedError

    def visit_fun(self, node):
        raise NotImplementedError

    def visit_call(self, node):
        raise NotImplementedError

    def visit_map(self, node):
        raise NotImplementedError

    def visit_get(self, node):
        raise NotImplementedError

    def visit_put(self, node):
        raise NotImplementedError

    def visit_keys(self, node):
        raise NotImplementedError

    def visit_list(self, node):
        raise NotImplementedError

    def visit_head(self, node):
        raise NotImplementedError

    def vist_tail(self, node):
        raise NotImplementedError

    def visit_push(self, node):
        raise NotImplementedError

    def visit_print(self, node):
        raise NotImplementedError

    def visit_type(self, ndoe):
        raise NotImplementedError

    def visit_nil(self, node):
        raise NotImplementedError
