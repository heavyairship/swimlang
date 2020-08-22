(mut x 20);
(func bar:
  0
);
(func foo y:
  (set x 2);
  (print (+ y x));
  (bar)
);
(foo x);
(let a "hi ");
(let b "there!");
(+ a b)