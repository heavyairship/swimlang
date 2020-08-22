(mut x 20);
(fun bar:
  0
);
(fun foo y:
  (set x 2);
  (print (+ y x));
  (bar)
);
(foo x);
(let a "hi ");
(let b "there!");
(+ a b)