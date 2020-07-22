func outer(a):
    func inner(x):
        2 + x
    end;
    inner
end;
func apply(f, x):
    call f(x)
end;
a := call outer(1);
call apply(a, 2)