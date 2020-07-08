import pandas as pd
import numpy as np
from functools import wraps


class TargetIntradaySerie:
    
    def __init__(self, freq, interval_time, delays, exclude_last=False):
        self.freq = freq
        self.interval_time = interval_time
        self.delays = delays
        self.exclude_last = exclude_last
        
        
    @property
    def freq(self):
        return self._freq
    
    @freq.setter
    def freq(self, freq):
        self._freq = freq
        self._filter_data = self._get_filter_data()
        
    @property
    def interval_time(self):
        return self._freq
    
    @interval_time.setter
    def interval_time(self, interval_time):
        self._interval_time = interval_time
        self._filter_interval_time = self._get_filter_interval_time()

        
    def build(self, data):
        
        data = self._check_data(data)
        filter_data = self._filter_interval_time(self._filter_data(data).dropna())
        dataframe = self._pivot_serie(filter_data)

        if not self.exclude_last:
            return dataframe[self.delays: ]
        
        return dataframe[self.delays: -1]
    
    def get_previous_data(self, data):
        
        data = self._check_data(data)
        filter_data = self._filter_interval_time(self._filter_data(data.shift()).dropna())
        serie = filter_data.groupby(filter_data.index.date).first().iloc[:, 0]
        
        if not self.exclude_last:
            return serie[self.delays: ]
        
        return serie[self.delays: -1]
        

    @classmethod
    def scale_and_build(cls, function):

        @wraps(function)
        def build_and_reshape(self, data, return_dataframe=False, expand=True, *args, **kwargs):
            
            if not isinstance(self, TargetIntradaySerie):
                raise ValueError('The class needs to inherit from TargetIntradaySerie')
            
            dataframe = self.build(data)
            array = function(self, dataframe.values.T, *args, **kwargs).T
            
            if expand:
                array = np.expand_dims(array, 2)
                    
            if return_dataframe:
                return array, dataframe
            
            return array
        
        return build_and_reshape
        
    def _pivot_serie(self, dataframe):
        return dataframe.pivot_table(values=dataframe.columns[0],
                                     index=dataframe.index.date,
                                     columns=dataframe.index.time) 


    def _get_filter_data(self):
        return lambda dataframe: dataframe.resample(self._freq).first()
    
    
    def _get_filter_interval_time(self):
        return lambda dataframe: dataframe.between_time(*self._interval_time)
    
    @staticmethod
    def _check_data(data):
        
        if isinstance(data, pd.Series):
            return data.to_frame('series_value')
        
        elif isinstance(data, pd.DataFrame) and (data.shape[1] == 1):
            return data
        
        raise ValueError('You must pass a Series or a Dataframe with one column.')
        