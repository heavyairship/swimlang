(let n  5);
(let fact 1);
(while (> n 1) (
    (set fact (* fact n));
    (set n (- n 1))
));
fact