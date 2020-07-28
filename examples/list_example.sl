(func identity l: 
    (if l
        (let h (head l));
        (let t (tail l));
        (push h (call identity t))
        []
    )
);

(func reverse l:
    (func helper l a:
        (if l
            (let h (head l));
            (let t (tail l));
            (call helper t (push h a))
            a
        )
    );
    (call helper l [])
);

(func sum l a:
    (if l
        (let h (head l));
        (let t (tail l));
        (+ h (call sum t 0))
        0
    )
);

(func len l a:
    (if l
        (let t (tail l));
        (+ 1 (call len t 0))
        0
    )
);

(func ave l:
    (/ (call sum l 0) (call len l 0))
);

(func map f l:
    (if l
        (let h (head l));
        (let t (tail l));
        (push (call f h) (call map f t))
        []
    );
);

(func filter f l:
    (if l
        (let h (head l));
        (let t (tail l));
        (let rest (call filter f t));
        (if (call f h)
            (push h rest)
            rest
        )
        []
    )
);

(func timestwo n: 
    (* 2 n)
);

(func even n:
    (== n (* 2 (/ n 2)))
);

(let in [1 2 3 4]);
(mut out (call map timestwo in));
(print out);
(set out (call filter even in));
(print out);

(let l [True 2 3]);
(print (call identity l));
(print (call reverse l));

(let l2 [1 2 3 4]);
(print (call ave l2))
