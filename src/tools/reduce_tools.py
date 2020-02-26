from functools import reduce
def repeated(f, n):
    def rfun(p):
        return reduce(lambda x, _: f(x), range(n), p)
    return rfun