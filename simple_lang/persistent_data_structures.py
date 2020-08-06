
##################################################################################
# Persistent List
##################################################################################


import pdb


class P_List(object):
    # FixMe: add iterator
    # FixMe: add [] operator
    # FixMe: add in operator
    class Node(object):
        def __init__(self, val, next):
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
        # FixMe: we can make this more efficient by not having a Node inner class.
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


class P_Tree(object):
    # FixMe: change this from a vanilla BST to a RBTree
    # FixMe: make this persistent
    # FixMe: add [] operator
    # FixMe: add in operator
    class Node(object):
        def __init__(self, key, val, parent):
            self._key = key
            self._val = val
            self._parent = parent
            self._left = None
            self._right = None
            self._next = None
            self._prev = None

        def str_helper(self, indent):
            curr = "  " * indent + str(self._key) + ": " + str(self._val)
            if self._left is None:
                left = "  " * (indent + 1) + "None"
            else:
                left = self._left.str_helper(indent + 1)
            if self._right is None:
                right = "  " * (indent + 1) + "None"
            else:
                right = self._right.str_helper(indent + 1)
            return curr + "\n" + left + "\n" + right

        def __str__(self):
            return self.str_helper(0)

        def put(self, key, val):
            hkey = hash(key)
            if hkey < hash(self._key):
                if self._left is None:
                    new = P_Tree.Node(key, val, self)
                    new._next = self
                    new._prev = self._prev
                    if self._prev is not None:
                        self._prev._next = new
                    self._prev = new
                    self._left = new
                else:
                    self._left.put(key, val)
            else:
                if self._right is None:
                    new = P_Tree.Node(key, val, self)
                    new._next = self._next
                    new._prev = self
                    if self._next is not None:
                        self._next._prev = new
                    self._next = new
                    self._right = new
                else:
                    self._right.put(key, val)

        def get(self, key):
            hkey = hash(key)
            self_hkey = hash(self._key)
            if hkey == self_hkey:
                return self._val
            if hkey < self_hkey:
                if self._left is None:
                    raise KeyError
                return self._left.get(key)
            else:
                if self._right is None:
                    raise KeyError
                return self._right.get(key)

        def first(self):
            curr = self
            while curr._left is not None:
                curr = curr._left
            return curr

    def __init__(self):
        self._root = None

    def __str__(self):
        return str(self._root)

    def put(self, key, val):
        if self._root is None:
            self._root = P_Tree.Node(key, val, None)
        else:
            self._root.put(key, val)

    def get(self, key):
        if self._root is None:
            raise KeyError
        return self._root.get(key)

    class Iterator(object):
        def __init__(self, curr):
            self._curr = curr

        def __iter__(self):
            return self

        def __next__(self):
            if self._curr is None:
                raise StopIteration
            out = self._curr._key
            self._curr = self._curr._next
            return out

    def first(self):
        if self._root is None:
            return None
        return self._root.first()

    def __iter__(self):
        return P_Tree.Iterator(self.first())


t = P_Tree()
t.put(4, "44")
l = [x for x in t]
print(l)

t.put(2, "22")
l = [x for x in t]
print(l)

t.put(6, "66")
l = [x for x in t]
print(l)

t.put(1, "11")
l = [x for x in t]
print(l)

t.put(3, "33")
l = [x for x in t]
print(l)

t.put(5, "55")
l = [x for x in t]
print(l)

t.put(7, "77")
l = [x for x in t]
print(l)

print(t)
