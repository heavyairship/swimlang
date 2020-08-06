
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
        count = 0

        def __init__(self, key, val):
            P_Tree.Node.count += 1
            self._key = key
            self._val = val
            self._left = None
            self._right = None

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
            self_hkey = hash(self._key)
            out = P_Tree.Node(self._key, self._val)
            if hkey == self_hkey:
                # FixMe: what about hash collisions? Really need a list here
                # of keys that have this hash
                out._left = self._left
                out._right = self._right
            elif hkey < self_hkey:
                if self._left is None:
                    out._left = P_Tree.Node(key, val)
                else:
                    out._left = self._left.put(key, val)
                out._right = self._right
            else:
                if self._right is None:
                    out._right = P_Tree.Node(key, val)
                else:
                    out._right = self._right.put(key, val)
                out._left = self._left
            return out

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

        def ordered(self, acc):
            # FixMe: make iterative
            if self._left:
                self._left.ordered(acc)
            acc.append(self._key)
            if self._right:
                self._right.ordered(acc)

    def __init__(self):
        self._root = None

    def __str__(self):
        return str(self._root)

    def put(self, key, val):
        out = P_Tree()
        if self._root is None:
            out._root = P_Tree.Node(key, val)
        else:
            out._root = self._root.put(key, val)
        return out

    def get(self, key):
        if self._root is None:
            raise KeyError
        return self._root.get(key)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __iter__(self):
        ordered = []
        if self._root is None:
            return iter(ordered)
        self._root.ordered(ordered)
        return iter(ordered)


t = P_Tree()
t1 = t.put(3, "33")
t2 = t1.put(1, "11")
t3 = t2.put(2, "22")
t4 = t3.put(5, "55")
t5 = t4.put(4, "44")
assert([(k, t[k]) for k in t] == [])
assert([(k, t1[k]) for k in t1] == [(3, "33")])
assert([(k, t2[k]) for k in t2] == [(1, "11"), (3, "33")])
assert([(k, t3[k]) for k in t3] == [(1, "11"), (2, "22"), (3, "33")])
assert([(k, t4[k]) for k in t4] == [
       (1, "11"), (2, "22"), (3, "33"), (5, "55")])
assert([(k, t5[k]) for k in t5] == [
    (1, "11"), (2, "22"), (3, "33"), (4, "44"), (5, "55")])
# Due to sharing where possible, we only need 11 total nodes, not 15, despite being immutable!
assert(P_Tree.Node.count == 11)

P_Tree.Node.count = 0
random_tree = P_Tree()
n = 1000
for i in range(n):
    import random
    random_tree = random_tree.put(int(random.random()*1000), i)
nodes_without_sharing = int((n*(n+1))/2)
nodes_with_sharing = P_Tree.Node.count
print("Used %d nodes total" % nodes_with_sharing)
print("Saved %d nodes by sharing (absolute)" %
      (nodes_without_sharing - nodes_with_sharing))
print("Needed %dx fewer nodes due to sharing (ratio)" %
      (nodes_without_sharing/nodes_with_sharing))
