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
    (while keylist (
        (set k (head keylist));
        (print k);
        (print (get m k));
        (set keylist (tail keylist));
    ));
);
(call printmap m4);

(if {4:4 2:2 1:1 3:3 6:6 5:5 7:7} 0 1)