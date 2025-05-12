def function1(a, b):
    return a + b + function3(a, a, a)

def function2(a, b, c):
    return c * function1(a, b) + sum(a, b)

def function3(a, b, c):
    return c * function2(a, b, c)
