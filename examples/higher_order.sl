(fun filter f l:
  (if l
    (let h (head l));
    (let t (tail l));
    (let rest (filter f t));
    (if (f h)
      (push h rest)
      (rest)
    )
    []
  )
);
(fun map f l:
  (if l
    (let h (head l));
    (let t (tail l));
    (push (f h) (map f t))
    []
  )
);
(fun fold_l f l a:
  (if l
    (let h (head l));
    (let t (tail l));
    (fold_l f t (f a h))
    a
  )
);
(fun fold_r f l a:
  (if l
    (let h (head l));
    (let t (tail l));
    (f h (fold_r f t a))
    a
  )
);
(let res (filter (fun gt10 x:
  (> x 0)
) [-3 -2 -1 0 1 2 3]));
(print res);
(let res2 (map (fun times2 x:
  (* 2 x)
) [1 2 3]));
(print res2);
(fun add a b:
  (+ a b)
);
(let res3 (fold_l add [1 2 3] 0));
(print res3);
(let res4 (fold_r add [1 2 3] 0));
(print res4)