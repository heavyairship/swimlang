(mut x 20);
(func bar: 
    0
);
(func foo y: (
    (set x 2);
    (+ y x);
    (call bar)
));
(call foo x)