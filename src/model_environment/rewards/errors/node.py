from inspect import isfunction

def check_valid_parameter(parameter):
    if  not isinstance(parameter, float) and  not isinstance(parameter, int):
        raise ValueError('You must pass int or float parameter')


def check_valid_function(function):
    if  function is not None and  not isfunction(function):
        raise ValueError('You must pass a instance of function')