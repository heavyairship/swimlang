(fun fact n:
  (if (< n 2)
    1
    (* n (fact (- n 1)))
  )
);
(fun choose n k:
  (/ (fact n) (* (fact (- n k)) (fact k)))
);
(print (choose 52 2));
(print (choose 52 52));
(print (choose 52 5));
(print (choose 52 10))