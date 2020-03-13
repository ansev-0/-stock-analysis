def inlist(var):
    if not isinstance(var,list) and (not isinstance (var, tuple)):
        return [var]
    return var

def join_values_filtered_by_keys(d,keys): 
    keys = inlist(keys)
    return '_'.join([v  for k, v in d.items() if k in keys])