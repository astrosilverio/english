def fact(n):
    if n <= 1:
        return 1
    else:
        return n * fact(n-1)


# Output
2 Compare n and 1
2 If n is lesser or equal to 1
3 Return 1
4 Else
5 Compute n minus 1
5 Call fact with result of n minus 1 as argument
5 Compute n times result of call to fact
5 Return result of n times call to fact

def foo(x):
    if x:
        return 'yes'

# Output
2 If x evaluates to True