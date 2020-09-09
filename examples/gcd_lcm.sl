(fun gcd a b:
  (fun helper a b:
    (let r (% a b));
    (if r
      (helper b r)
      b
    )
  );
  (if (|| (== a 0) (== b 0))
    0
    (if (> a b)
      (helper a b)
      (helper b a)
    )
  )
);
(fun lcm a b:
  (/ (* a b) (gcd a b))
);
(lcm (* 2 17) (* 2 11))