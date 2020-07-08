import numpy as np
import pandas as pd

class DataFrameAcurracyForecasting:
    
    def __init__(self, dataframe, init_value):
        
        self._real_diff = None
        self._pred_diff = None
        self.__hit_serie = None
        self._accuracy_pred = None
        self.init_value = init_value
        self.dataframe = dataframe
        
    @property
    def dataframe(self):
        return self._dataframe
    
    @property
    def real_diff(self):
        return self._real_diff
    
    
    @property
    def pred_diff(self):
        return self._pred_diff
    
    @property
    def hit_serie(self):
        return self.__hit_serie

    @property
    def accuracy_pred(self):
        return self._accuracy_pred
    
    @dataframe.setter
    def dataframe(self, dataframe):
        self.__check_valid_columns(dataframe)
        self._dataframe = dataframe
        self._real_diff = self.__calulate_real_incr()
        self._pred_diff = self.__calculate_pred_incr()
        self.__hit_serie, self._accuracy_pred = self.__calculate_accuracy_incr()
        
    def __calulate_real_incr(self):
        return (self.dataframe['real']
                    .diff()
                    .fillna(self.dataframe['real'].iloc[0] - self.init_value))
        
    def __calculate_pred_incr(self):
        return (self.dataframe['pred'].sub(self.dataframe['real'].shift())
                    .fillna(self.dataframe['pred'].iloc[0] - self.init_value))
    
    def __calculate_accuracy_incr(self):
        hit = np.sign(self._real_diff).eq(np.sign(self._pred_diff))
        return hit, hit.mean()
    
    @staticmethod
    def __check_valid_columns(dataframe):
        columns=dataframe.columns.tolist()
        if  not sorted(columns) == ['pred', 'real']:
            raise(ValueError, f'Columns must be: pred and real, you have passed: {columns}')