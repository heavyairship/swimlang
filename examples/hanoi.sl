(let dtoc {
  0:"0"
  1:"1"
  2:"2"
  3:"3"
  4:"4"
  5:"5"
  6:"6"
  7:"7"
  8:"8"
  9:"9"
});
(fun itoa n:
  (let q (/ n 10));
  (let r (% n 10));
  (let rc ((get dtoc r)));
  (if (> q 0)
    (+ (itoa q) rc)
    rc
  )
);
(fun concat l:
  (if l
    (+ (head l) (concat (tail l)))
    ""
  )
);
(fun move n src dst:
  (print (concat (["Moved " (itoa n) " from " src " to " dst])))
);
(fun move_via n src via dst:
  (if (> n 0)
    (move_via (- n 1) src dst via);
    (move n src dst);
    (move_via (- n 1) via src dst)
    Nil
  )
);
(fun solve n:
  (move_via n "A" "B" "C")
);
(solve 3)