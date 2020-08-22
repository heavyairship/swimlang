(func factorial n:
  (if (|| (== n 0) (== n 1))
    1
    (* n (factorial (- n 1)))
  )
);
(factorial 6)