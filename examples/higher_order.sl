(func sumfactory: 
    (func sum a b: 
        (+ a b)
    );
    sum
);
(func apply f x y:
    (call f x y)
);
(call apply (call sumfactory) 1 2)