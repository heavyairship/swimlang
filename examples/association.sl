(mut a {});
(set a (put a 1 1));
(set a (put a "b" [2 3 4]));
(print a);
(get a "b");
(let l []);
(set a (put a l 1));
(get a l)