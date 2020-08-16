(let m {});
(let m1 (put m "0" 0));
(let m2 (put m1 "1" 1));
(let m3 (put m2 0 "0"));
(let m4 (put m3 1 "1"));
(print m);
(print m1);
(print m2);
(print m3);
(print m4);
(func f m:
  (get m 0)
);
(call f m4);
(func printmap m:
  (mut keylist (keys m));
  (mut k nil);
  (while keylist
    (set k (head keylist));
    (print k);
    (print (get m k));
    (set keylist (tail keylist))
  )
);
(call printmap m4);
(if {
  1:1
  2:2
  3:3
  4:4
  5:5
  6:6
  7:7
}
  0
  1
)