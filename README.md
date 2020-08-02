# SimpleLang
Simple functional programming language interpreter for fun! Supports (higher order) functions, closures, Currying, variable bindings with lexical scoping rules, lists, maps, arithmetic, boolean logic, strings, while-loops, conditionals, sequencing, etc. 

### Here's an example

```
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

(func map f l:
    (if l
        (let h (head l));
        (let t (tail l));
        (push (call f h) (call map f t))
        []
    )
);

(func timestwo n: 
    (* 2 n)
);

(let l [1 2 3 4]);
(call reverse (call map timestwo l))
```

The above code evaluates to the list `[8 6 4 2]`.
