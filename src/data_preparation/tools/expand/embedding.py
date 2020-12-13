import pandas as pd
import numpy as np
from functools import wraps


class EmbedTimeSeries:

    def __init__(self, embed_dim=None, lag=1, step=1):
        self.step=step
        self.lag = lag
        self.embed_dim = embed_dim

    @property 
    def min_len(self):
        return self._min_len

    @property 
    def embed_dim(self):
        return self._embed_dim

    @embed_dim.setter
    def embed_dim(self, embed_dim):
        self._embed_dim = embed_dim
        self._min_len = (self._embed_dim - 1) * self.lag + 1


    def __call__(self, data, ndmin=None, pos_add_dims='right'):
        len_data = data.shape[0]
        data = np.asarray(data)
        len_start_index = len_data - self._min_len + 1
        len_embed = (len_start_index - 1) // self.step + 1
        index = np.repeat([np.arange(self.embed_dim) * self.lag], len_embed, axis=0)
        index += np.arange(start=0, stop=len_start_index, step=self.step)[:, None]
        array = data[index]
        
        #check ndmin
        if (ndmin is not None) and (array.ndim < ndmin):
            add_dims = ndmin - array.ndim

            if pos_add_dims == 'right':
                return self._add_right_dims(array, add_dims)
            elif pos_add_dims == 'left':
                return self._add_left_dims(array, add_dims)
            else:
                raise ValueError('Invalid pos_add_dim, you must pass right or left')
            
        return array

    @staticmethod
    def _add_right_dims(array, dims):
        return array.reshape(*array.shape, *[1] * dims)

    @staticmethod
    def _add_left_dims(array, dims):
        return array.reshape(*[1] * dims, *array.shape)






        
        


    