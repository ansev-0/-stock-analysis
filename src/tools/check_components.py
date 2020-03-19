
def check_equal_lengths(*args):
    if len(set(map(len, args)))>1: raise ValueError


def eval_type_argument(type_arg):
    if isinstance(type_arg, str):
        try:
            type_arg = eval(type_arg)
        except Exception:
            pass
    if type(type_arg) != type:
        raise ValueError('Invalid type argument')
    return type_arg

