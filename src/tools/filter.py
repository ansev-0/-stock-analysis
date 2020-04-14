def filter_valid_kwargs(kwargs, valid_keys):
    return dict(filter(lambda kwarg: kwarg[0] in valid_keys, kwargs.items()))

def filter_valid_kwarg(kwargs, valid_key):
    return dict(filter(lambda kwarg: kwarg[0] in valid_key, kwargs.items()))



def filter_dict(dictionary, kfilter):
    if isinstance(kfilter, str):
        return filter_valid_kwarg(dictionary, kfilter)
    return filter_valid_kwarg(dictionary, kfilter)