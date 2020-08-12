(let l [[] [1] 2 "a" (func f:
  (print "hi")
)]);
(call (head (tail (tail (tail (tail l))))));
l