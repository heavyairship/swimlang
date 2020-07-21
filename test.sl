counter := 0;
y := 0;
z := while(counter < 10 && 1 == 1 || 0 > 15):
    counter := counter + 1;
    if(4 < counter && counter < 7):
        y := y - 2
    else:
        y := y - 1
    end
end;
z;
x:= 1+6*2; 
y:= 2*2+2;
x;
z;
foo := 5;
bar := 1;
while((foo := foo - 1) >= 0):
    x := 2;
    while((x := x - 1) >= 0):
        bar := bar * 2
    end
end;
if(True):
    1
else:
    2
end;
bar