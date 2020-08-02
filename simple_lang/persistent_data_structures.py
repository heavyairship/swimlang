
##################################################################################
# Persistent List
##################################################################################


class P_List(object):
    class Node(object):
        def __init__(self, val, next):
            if not (type(next) is P_List.Node or next is None):
                raise TypeError
            self._val = val
            self._next = next

        def __str__(self):
            return str(self._val)

    def __init__(self, _head=None):
        if not (type(_head) is P_List.Node or _head is None):
            raise TypeError
        self._head = _head

    def head(self):
        if self._head is None:
            raise ValueError("`%s` is illegal on empty list" %
                             self.head.__name__)
        return self._head._val

    def tail(self):
        # We can make this more efficient by not having a Node inner class.
        # If we just have P_Lists, tail doesn't need to make a new object at all.
        if self._head is None:
            raise ValueError("`%s` is illegal on empty list" %
                             self.tail.__name__)
        return P_List(self._head._next)

    def push(self, val):
        return P_List(P_List.Node(val, self._head))

    def __str__(self):
        curr = self._head
        out = ""
        first = True
        while curr is not None:
            if first:
                first = False
            else:
                out += " "
            out += str(curr)
            curr = curr._next
        return "[" + out + "]"
