(fun nested_len l:
  (if l
    (let h (head l));
    (let t (tail l));
    (+ (if (== (type h) "List")
      (nested_len h)
      1
    ) (nested_len t))
    0
  )
);
(print (nested_len [1 [2 3]]));
(print (nested_len [1 [2 [3 4]]]));
(print (nested_len [1 [2 [3 [4 [5 6]]]]]));
(print (nested_len [1 [2] 1 [2] 1]))