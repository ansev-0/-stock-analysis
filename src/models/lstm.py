from functools import reduce
from keras.layers.recurrent import LSTM, Conv1D
def stacked_lstm(array_input, list_dict_params, **kwargs):
    return reduce(lambda previous_tensor, new_params: LSTM(**new_params, **kwargs)(previous_tensor),
                  list_dict_params, array_input)


def parallel_conv1d(array_input, list_dict_params, **kwargs):
    return list(map(lambda conv: Conv1D(**conv, **kwargs)(array_input) ,list_dict_params))