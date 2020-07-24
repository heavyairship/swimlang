(let n  5);
(let fact 1);
(while (> n 1) (
    (let fact (* fact n));
    (let n (- n 1))
));
fact