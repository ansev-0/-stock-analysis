import numpy as np
import pandas as pd

class FinancialArray:
    
    def __init__(self, array, index_of_main_frecuency, index_array):
        
        self._index_of_main_frecuency = index_of_main_frecuency
        self._mapper_list = None
        self._mapper_array = None
        self._array = array
        self.index_array = index_array
        
        assert len(array) == len(index_array)
        
    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, array):
        self._array = array

    @property
    def shape(self):
        return self._array.shape
        
    @property
    def index_of_main_frecuency(self):
        return self._index_of_main_frecuency
    
    @property
    def index_array(self):
        return self._index_array
    
    @index_array.setter
    def index_array(self, index_array):
        self._index_array = index_array
        self._mapper_array = self._index_array.to_series()\
            .reindex(self._index_array.union(self._index_of_main_frecuency)).ffill()\
            .loc[self._index_of_main_frecuency]
        assert  not np.isnan(self._mapper_array).any()

        self._mapper_list = self._mapper_array.map(dict(zip(self._index_array, 
                                                            range(len(self._index_array))))).tolist()
        
    def __getitem__(self, index):
        return self._array[self._mapper_list[index]]