(let l [[] [1] 2 "a" (fun f:
  (print "hi")
)]);
((head (tail (tail (tail (tail l))))));
l