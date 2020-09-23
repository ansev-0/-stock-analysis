def filter_valid_kwargs(kwargs, valid_keys):
    return dict(filter(lambda kwarg: kwarg[0] in valid_keys, kwargs.items()))


def filter_dict(dictionary, kfilter):
    if not isinstance(kfilter, tuple) and not isinstance(kfilter, list):
        return filter_valid_kwargs(dictionary, (kfilter, ))
    return filter_valid_kwargs(dictionary, kfilter)