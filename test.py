from simple_lang import *


def visitors():
    return [Printer(), Evaluator()]


# Test tokenizer/parser
print("**********")
src = """(let count 0);
(let y 1);
(while (|| (< count 10) (> 1 2)) (
    (set count (+ count 1));
    (set y (if (&& (< 2 count) (< count 7)) (+ y 0) (+ y 1)))
));
y
"""
tokenizer = Tokenizer(src)
tokens = tokenizer.tokenize()
parser = Parser(tokens)
node = parser.parse()
for v in visitors():
    print(v(node))

# Test arithmetic/bool statements
print("**********")
node1 = Mul(Int(2), Int(3))  # 6
node2 = Add(Int(2), Int(3))  # 5
node3 = Add(node1, Mul(node1, node2))
node4 = Eq(Int(31), node3)
node5 = Or(node4, Eq(Int(1), Int(1)))
node6 = And(Not(node5), node5)
for v in visitors():
    print(v(node6))

# Test if statements
print("**********")
node1 = If(Bool(True), Bool(True), Int(2))
node2 = If(Bool(False), node1, Int(3))
node3 = If(Bool(True), node2, node2)
for v in visitors():
    print(v(node2))

# Test assign
print("**********")
node1 = Let(Var("x"), Add(Int(1), Int(1)))
for v in visitors():
    print(v(node1))

# Test seq
print("**********")
node1 = Let(Var("x"), Add(Int(1), Int(1)))
node2 = Let(Var("b"), Bool(True))
node3 = Set(Var("x"), Add(Var("x"), Int(10)))
node4 = Set(Var("x"), Add(Var("x"), Int(20)))
node5 = If(Var("b"), node3, node4)
node6 = Seq(node1, node2)
node7 = Seq(node5, Var("y"))
node8 = Seq(node6, node7)
for v in visitors():
    print(v(node8))

# Test while statements
print("**********")
node1 = Let(Var("x"), Int(0))
node2 = Set(Var("x"), Add(Var("x"), Int(1)))
node3 = While(NotEq(Var("x"), Int(10)), node2)
node4 = Seq(node1, node3)
for v in visitors():
    print(v(node4))
print("**********")
