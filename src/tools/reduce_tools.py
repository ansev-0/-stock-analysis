from functools import reduce
def repeated(f, n):
    def rfun(p):
        return reduce(lambda x, _: f(x), range(n), p)
    return rfun

def flatten_adding(elements):
    return reduce(lambda cum, new: cum + new, elements)

def combine_dicts(*args):
    return reduce(lambda cum_dict, new_dict: dict(cum_dict, **new_dict), args)