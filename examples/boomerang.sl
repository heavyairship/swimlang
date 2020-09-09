(fun len l:
  (if l
    (+ 1 (len (tail l)))
    0
  )
);
(fun boomerang l:
  (if (>= (len l) 3)
    (let a (head l));
    (let b (head (tail l)));
    (let c (head (tail (tail l))));
    (let t (tail l));
    (if (&& (== a c) (!= a b))
      (+ 1 (boomerang t))
      (boomerang t)
    )
    0
  )
);
(print (boomerang [3 7 3 2 1 5 1 2 2 -2 2]));
(print (boomerang [1 7 1 7 1 7 1]))