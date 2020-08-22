(fun mod m n:
  (mut o m);
  (while (>= o n)
    (set o (- o n))
  );
  o
);
(print "******************");
(print "fizzbuzz iterative");
(print "******************");
(mut i 1);
(mut o "");
(while (<= i 100)
  (set o "");
  (if (!(mod i 3))
    (set o "fizz")
    0
  );
  (if (!(mod i 5))
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
  (let o (if (&& (!(mod n 3)) (!(mod n 5)))
    "fizzbuzz"
    (if (!(mod n 3))
      "fizz"
      (if (!(mod n 5))
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