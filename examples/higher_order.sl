(fun sumfactory:
  (fun sum a b:
    (+ a b)
  );
  sum
);
(fun apply f x y:
  (f x y)
);
(apply (sumfactory) 1 2)