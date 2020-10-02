(fun join s l:
    (if l
        (let h (head l));
        (let t (tail l));
        (if t
            (+ (+ h s) (join s t))
            h
        )
        ""
    )
);

(fun rev l:
    (fun helper l a:
        (if l
            (let h (head l));
            (let t (tail l));
            (helper t (push h a))
            a
        )
    );
    (helper l [])
);

(fun len l:
    (if l
        (+ 1 (len (tail l)))
        0
    )
);

(fun fibstr n base:
    (fun helper n a:
        (if (! n)
            a
            (let first (head a));
            (let second (head (tail a)));
            (helper (- n 1) (push (+ first second) a))
        )
    );
    (let nvalid (>= n 2));
    (let lvalid (&& (== "List" (type base)) (== 2 (len base))));
    (let valid (&& nvalid lvalid));
    (if (! (nvalid))
        Nil
        (let first (head base));
        (let second (head (tail base)));
        (join ", " (rev (helper (- n 2) [second first])))
    )
);

(print (fibstr 3 ["j" "h"])); # "j, h, hj"

(print (fibstr 5 ["e" "a"])); # "e, a, ae, aea, aeaae"

(print (fibstr 6 ["n" "k"])) # "n, k, kn, knk, knkkn, knkknknk"