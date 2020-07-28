(mut n  5);
(mut fact 1);
(while (> n 1) (
    (set fact (* fact n));
    (set n (- n 1))
));
fact