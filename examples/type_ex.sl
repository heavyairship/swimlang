(print (type 1));
(print (type (+ 1 2)));
(print (type "hi"));
(print (type []));
(print (type (tail [1 2 3])));
(print (type {}));
(print (type (keys {
  1:2
  3:4
})));
(print (type Nil));
(print (type True));
(print (type (fun f:
  1
)))