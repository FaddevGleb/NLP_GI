def f(a, b, *args):
    print(type(args), args)

f(1, 2, [1, 2, 3])