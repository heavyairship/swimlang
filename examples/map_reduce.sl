(let f ["x" "x" "x" "x" "a" "b" "c" "d" "e" "a" "b" "c"]);
(fun map f:
  (if f
    (let h (head f));
    (let t (tail f));
    (push [h 1] (map t))
    []
  )
);
(fun in m k:
  (fun helper l:
    (if l
      (let h (head l));
      (let t (tail l));
      (if (== h k)
        True
        (helper t)
      )
      False
    )
  );
  (let ks (keys m));
  (helper ks)
);
(fun reduce l:
  (if l
    (let t (tail l));
    (let m (reduce t));
    (let e (head l));
    (let k (head e));
    (let v (head (tail e)));
    (let currv (if (in m k)
      (get m k)
      0
    ));
    (put m k (+ currv v))
    {}
  )
);
(let l (map f));
(let o (reduce l))