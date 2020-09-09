(fun prime n:
  (fun helper k:
    (if (== k 1)
      True
      (if (== (% n k) 0)
        False
        (helper (- k 1))
      )
    )
  );
  (&& (>= n 2) (helper (/ n 2)))
);
(fun print_primes n:
  (if (== 1 n)
    Nil
    (print_primes (- n 1));
    (if (prime n)
      (print n)
      Nil
    )
  )
);
(fun int_sqrt_ceil n:
  (if (|| (== n 0) (== n 1))
    n
    (mut i 1);
    (while (< (* i i) n)
      (set i (+ i 1))
    )
  )
);
(fun prime_it n:
  (if (< n 2)
    False
    (mut d 2);
    (mut rtn True);
    (while (&& rtn (<= d (int_sqrt_ceil n)))
      (if (% n d)
        Nil
        (set rtn False)
      );
      (set d (+ d 1))
    );
    rtn
  )
);
(fun print_primes_it n:
  (mut cur 2);
  (while (<= cur n)
    (if (prime_it cur)
      (print cur)
      Nil
    );
    (set cur (+ cur 1))
  );
  Nil
);
(print_primes_it 100)