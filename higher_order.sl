func sumfactory():

    func sum(a, b):
        a + b
    end;

    sum
end;

func apply(f, x, y):
    call f(x, y)
end;

call apply(call sumfactory(), 1, 2)