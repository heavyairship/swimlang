(func identity l:
  (if l
    (let h (head l));
    (let t (tail l));
    (push h (identity t))
    []
  )
);
(func reverse l:
  (func helper l a:
    (if l
      (let h (head l));
      (let t (tail l));
      (helper t (push h a))
      a
    )
  );
  (helper l [])
);
(func sum l a:
  (if l
    (let h (head l));
    (let t (tail l));
    (+ h (sum t 0))
    0
  )
);
(func len l a:
  (if l
    (let t (tail l));
    (+ 1 (len t 0))
    0
  )
);
(func ave l:
  (/ (sum l 0) (len l 0))
);
(func map f l:
  (if l
    (let h (head l));
    (let t (tail l));
    (push (f h) (map f t))
    []
  )
);
(func filter f l:
  (if l
    (let h (head l));
    (let t (tail l));
    (let rest (filter f t));
    (if (f h)
      (push h rest)
      rest
    )
    []
  )
);
(func timestwo n:
  (* 2 n)
);
(func even n:
  (== n (* 2 (/ n 2)))
);
(let in [1 2 3 4]);
(mut out (map timestwo in));
(print out);
(set out (filter even in));
(print out);
(let l [True 2 3]);
(print (identity l));
(print (reverse l));
(let l2 [1 2 3 4]);
(print (ave l2))