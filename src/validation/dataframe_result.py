import numpy as np
import pandas as pd

class DataFrameAcurracyForecasting:
    
    def __init__(self, dataframe, init_value):
        
        self._real_diff = None
        self._test_diff = None
        self.__hit_serie = None
        self._accuracy_test = None
        self.init_value = init_value
        self.dataframe = dataframe
        
    @property
    def dataframe(self):
        return self._dataframe
    
    @property
    def real_diff(self):
        return self._real_diff
    
    
    @property
    def test_diff(self):
        return self._test_diff
    
    @property
    def hit_serie(self):
        return self.__hit_serie

    @property
    def accuracy_test(self):
        return self._accuracy_test
    
    @dataframe.setter
    def dataframe(self, dataframe):
        self.__check_valid_columns(dataframe)
        self._dataframe = dataframe
        self._real_diff = self.__calulate_real_incr()
        self._test_diff = self.__calculate_test_incr()
        self.__hit_serie, self._accuracy_test = self.__calculate_accuracy_incr()
        
    def __calulate_real_incr(self):
        return (self.dataframe['real']
                    .diff()
                    .fillna(self.dataframe['real'].iloc[0] - self.init_value))
        
    def __calculate_test_incr(self):
        return (self.dataframe['test'].sub(self.dataframe['real'].shift())
                    .fillna(self.dataframe['test'].iloc[0] - self.init_value))
    
    def __calculate_accuracy_incr(self):
        hit = np.sign(self._real_diff) == np.sign(self._test_diff)
        return hit, hit.mean()
    
    @staticmethod
    def __check_valid_columns(dataframe):
        columns=dataframe.columns.tolist()
        if  not sorted(columns) == ['real', 'test']:
            raise(ValueError)