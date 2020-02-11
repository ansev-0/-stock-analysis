def check_equal_lengths(*args):
    if len(set(map(len,args)))>1: raise ValueError