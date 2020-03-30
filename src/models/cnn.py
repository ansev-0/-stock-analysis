from keras.layers import Conv1D

def parallel_conv1d(array_input, list_dict_params, **kwargs):
    return list(map(lambda conv: Conv1D(**conv, **kwargs)(array_input) ,list_dict_params))