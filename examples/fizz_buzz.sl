(print "******************");
(print "fizzbuzz iterative");
(print "******************");
(mut i 1);
(mut o "");
(while (<= i 100)
  (set o "");
  (if (!(% i 3))
    (set o "fizz")
    0
  );
  (if (!(% i 5))
    (set o (+ o "buzz"))
    0
  );
  (if (== o "")
    (set o i)
    0
  );
  (print o);
  (set i (+ i 1))
);
(print "******************");
(print "fizzbuzz recursive");
(print "******************");
(fun fizzbuzz n:
  (let o (if (&& (!(% n 3)) (!(% n 5)))
    "fizzbuzz"
    (if (!(% n 3))
      "fizz"
      (if (!(% n 5))
        "buzz"
        n
      )
    )
  ));
  (print o);
  (if (== n 100)
    Nil
    (fizzbuzz (+ n 1))
  )
);
(fizzbuzz 1)