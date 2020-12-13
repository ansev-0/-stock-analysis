from keras.layers.recurrent import LSTM
from functools import reduce

def stacked_lstm(array_input, list_dict_params, **kwargs):
    return reduce(lambda previous_tensor, new_params: LSTM(**new_params, **kwargs)(previous_tensor),
                  list_dict_params, array_input)



