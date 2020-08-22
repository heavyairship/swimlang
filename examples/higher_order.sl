(func sumfactory:
  (func sum a b:
    (+ a b)
  );
  sum
);
(func apply f x y:
  (f x y)
);
(apply (sumfactory) 1 2)