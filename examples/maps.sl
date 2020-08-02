(let m {});
(put m "0" 0);
(put m "1" 1);
(put m 0 "0");
(put m 1 "1");
(print m);
(print (get m 0));
(print (get m "0"));