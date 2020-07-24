(let x 0);
(let y 1);
(while (< x 10) (
    (let y (* y 2));
    (let x (+ x 1))
));
y;;