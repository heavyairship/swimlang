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
(fun row_for n k:
  (let na (itoa (* n k)));
  (if (== n 1)
    na
    (+ (+ (row_for (- n 1) k) "\t") na)
  )
);
(fun print_times_tbl_helper n k:
  (let row (row_for n k));
  (if (== n k)
    row
    (+ (+ row "\n") (print_times_tbl_helper n (+ k 1)))
  )
);
(fun print_times_tbl n:
  (print_times_tbl_helper n 1)
);
(print_times_tbl 12)