(let x 20);
(func foo y: (
    (set x 2);
    (+ y x)
));
(call foo x)