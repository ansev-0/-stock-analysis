import numpy as np
import pandas as pd

class FinancialArray:
    
    def __init__(self, array, index_of_main_frecuency, index_array):
        
        self._index_of_main_frecuency = index_of_main_frecuency
        self._mapper_array = None
        self._array = array
        self.index_array = index_array
        
        assert len(array) == len(index_array)
        
    @property
    def index_of_main_frecuency(self):
        return self._index_of_main_frecuency
    
    @property
    def index_array(self):
        return self._index_array
    
    @index_array.setter
    def index_array(self, index_array):
        self._index_array = index_array
        self._mapper_array = self._index_array.to_series().\
            reindex(self._index_of_main_frecuency).ffill().to_numpy()
        assert  not np.isnan(self._mapper_array).any()
        
    def __getitem__(self, index):
        return self._array[np.argmax(self._index_array == self._mapper_array[index])]