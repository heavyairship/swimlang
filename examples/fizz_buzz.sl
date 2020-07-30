(func mod m n:
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
  (if (! (call mod i 3))
    (set o "fizz")
    0
  );
  (if (! (call mod i 5))
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
(func fizzbuzz n: 
  (let o
    (if (&& (! (call mod n 3)) (! (call mod n 5)))
      "fizzbuzz"
      (if (! (call mod n 3))
        "fizz"
        (if (! (call mod n 5))
          "buzz"
          n
        )
      )
    )
  );
  (print o);
  (if (== n 100)
    0
    (call fizzbuzz (+ n 1))
  )
);
(call fizzbuzz 1);

0
