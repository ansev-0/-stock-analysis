from functools import wraps
from src.tools.filter import filter_valid_kwargs
import pandas as pd
import numpy as np



class AggregateDataFrame:
    
    def __init__(self, serie):
        self.serie = serie

    @classmethod
    def _get_dataframe(cls, function, *args, **kwargs):
        
        @wraps(function)
        def agg_function(self, agg_values=None, *args, **kwargs):
            return  pd.concat([function(self, agg_value=val, *args , **kwargs)
                               for val in agg_values], axis=1)
        return agg_function

class WindowEwm(AggregateDataFrame):

    @classmethod
    def get_ewm(cls, function):

        @wraps(function)
        @AggregateDataFrame._get_dataframe
        def ewm(self, agg_value, param_type='com', *args, **kwargs):
            
            return  (function(self,
                              self.serie.ewm(**{param_type : agg_value},
                                             **self.valid_kwargs(kwargs)), 
                                             *args, **kwargs)
                     .rename(f'ewm_{param_type}_{agg_value}_{function.__name__}'))
        return ewm
    
    def valid_kwargs(self, kwargs):
        valid_keys =  [key for key in self.serie.ewm.__code__.co_varnames[1:] 
                       if key not in ['com', 'halflife', 'span']]
        return filter_valid_kwargs(kwargs=kwargs,
                                   valid_keys=valid_keys)
    


    
class WindowRolling(AggregateDataFrame):

    @classmethod
    def get_rolling(cls, function):

        @wraps(function)
        @AggregateDataFrame._get_dataframe
        def rolling(self, agg_value, *args, **kwargs):
            valid_kwargs = self.valid_kwargs(kwargs)
            win_type = self._win_type(valid_kwargs)
            return  function(self, self.serie.rolling(window=agg_value,
                                                      **valid_kwargs),
                             *args, **kwargs).rename(f'rolling_{win_type}_{agg_value}_{function.__name__}')

        return rolling
    
    def valid_kwargs(self, kwargs):
        valid_keys =  [key for key in self.serie.rolling.__code__.co_varnames[1:] 
                       if key not in ['window']]
        return filter_valid_kwargs(kwargs=kwargs,
                                   valid_keys=valid_keys)
    @staticmethod
    def _win_type(valid_kwargs):
            try:
                return valid_kwargs['win_type']
            except KeyError:
                return ''


class AggregateWindowEwm(WindowEwm):
    
    @WindowEwm.get_ewm
    def mean(self, x=None, *args, **kwargs):
        return x.mean(*args, **kwargs)
    
    @WindowEwm.get_ewm
    def std(self, x=None, *args, **kwargs):
        return x.std(*args, **kwargs)
    
    @WindowEwm.get_ewm
    def var(self, x=None, *args, **kwargs):
        return x.var(*args, **kwargs)
    
    @WindowEwm.get_ewm
    def corr(self, x=None, *args, **kwargs):
        return x.corr(*args, **kwargs)
    
    @WindowEwm.get_ewm
    def cov(self, x=None, *args, **kwargs):
        return x.corr(*args, **kwargs)
    
class AggregateWindowRolling(WindowRolling):
    
    @WindowRolling.get_rolling
    def mean(self, x=None, *args, **kwargs):
        return x.mean(*args, **kwargs)
    
    @WindowRolling.get_rolling
    def std(self, x=None, *args, **kwargs):
        return x.std()
    
    @WindowRolling.get_rolling
    def var(self, x=None, *args, **kwargs):
        return x.var()
    
    @WindowRolling.get_rolling
    def corr(self, x=None, *args, **kwargs):
        return x.corr()
    
    @WindowRolling.get_rolling
    def sum(self, x=None, *args, **kwargs):
        return x.sum(*args, **kwargs)
    
    @WindowRolling.get_rolling
    def count(self, x=None, *args, **kwargs):
        return x.count()
    
    @WindowRolling.get_rolling
    def min(self, x=None, *args, **kwargs):
        return x.min(*args, **kwargs)
    
    @WindowRolling.get_rolling
    def max(self, x=None, *args, **kwargs):
        return x.max(*args, **kwargs)
    
    @WindowRolling.get_rolling
    def median(self, x=None, *args, **kwargs):
        return x.median(*args, **kwargs)
    
    @WindowRolling.get_rolling
    def quantile(self, x=None, *args, **kwargs):
        return x.quantile(*args, **kwargs)
    
    
    @WindowRolling.get_rolling
    def skew(self, x=None, *args, **kwargs):
        return x.skew(**kwargs)
    
    @WindowRolling.get_rolling
    def kurt(self, x=None, *args, **kwargs):
        return x.median(**kwargs)
    
