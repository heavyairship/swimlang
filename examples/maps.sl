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