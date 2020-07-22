func factorial(n):
   if(n == 0 || n == 1):
       1
   else:
       n * call factorial(n - 1)
   end
end;

call factorial(6)