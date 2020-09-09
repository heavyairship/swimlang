(fun concat l1 l2:
  (fun helper l:
    (if l
      (push (head l) (helper (tail l)))
      l2
    )
  );
  (helper l1)
);
(concat [1 2 3] [4 5 6])