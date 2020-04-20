def map_dict_from_underscore(dict_to_map, function, n, default_key):

    key_map = function.split('_')[n]
    try:
        return dict_to_map[key_map]
    except KeyError:
        return  dict_to_map[default_key]

def switch_none(var_None,var_else):
    
    if var_None is not None:
        return var_None
    else:
        return var_else
