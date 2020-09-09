(fun len l:
  (if l
    (+ 1 (len (tail l)))
    0
  )
);
(fun sum l:
  (if l
    (let h (head l));
    (let t (tail l));
    (+ h (sum t))
    0
  )
);
(fun prod l:
  (if l
    (let h (head l));
    (let t (tail l));
    (* h (prod t))
    1
  )
);
(fun digits n:
  (fun helper n a:
    (if (< n 10)
      (push n a)
      (let r (% n 10));
      (let q (/ n 10));
      (helper q (push r a))
    )
  );
  (helper n [])
);
(fun prod_of_digit l:
  (fun helper n:
    (let d (digits n));
    (if (== (len d) 1)
      (head d)
      (helper (prod d))
    )
  );
  (helper (sum l))
);
(prod_of_digit [123 123])