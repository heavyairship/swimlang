(func identity l: 
    (if l
        (let h (head l));
        (let t (tail l));
        (push h (call identity t))
        []
    )
);

(func reverse l a:
    (if l
        (let h (head l));
        (let t (tail l));
        (call reverse t (push h a))
        a
    )
);

(let l [True 2 3]);
(print (call identity l));
(print (call reverse l []))
