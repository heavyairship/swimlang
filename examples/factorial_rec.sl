(func factorial n:
  (if (|| (== n 0) (== n 1))
    1
    (* n (call factorial (- n 1)))
  )
);
(call factorial 6)