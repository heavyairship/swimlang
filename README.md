# SimpleLang
Simple functional programming language interpreter for fun! Supports (higher order) functions, closures, currying, variable bindings with lexical scoping rules, lists, maps, arithmetic, boolean logic, strings, while-loops, conditionals, sequencing, etc. Lists and maps are implemented with persistent data structures.

### Here's an example

```
(fun reverse l:
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

(fun map f l:
    (if l
        (let h (head l));
        (let t (tail l));
        (push (f h) (map f t))
        []
    )
);

(fun timestwo n: 
    (* 2 n)
);

(let l [1 2 3 4]);
(reverse (map timestwo l))
```

The above code evaluates to the list `[8 6 4 2]`.
