(mut n 8);
(mut log2n 0);
(while(> n 1)
  (set n (/ n 2));
  (set log2n (+ log2n 1))
);
log2n