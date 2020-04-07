import pandas as pd
import numpy as np

class StackedSerieDelay:

    def __init__(self, range_delays, zero_include=True):
        self.range_delays = range_delays

    def dataframe(self, serie, prefix):
        return self._get_dataframe(serie, prefix)

    def dataframe_without_nan(self,serie, prefix=True):
        return self._get_dataframe(serie, prefix).dropna()

    def array(self, serie):
        return self._get_array(serie)
    
    def array_without_nan(self, serie):
        array_with_nans = self._get_array(serie)
        return array_with_nans[~np.isnan(array_with_nans).any(axis=1)]

    def _get_dataframe(self, serie, prefix):
        dataframe = pd.concat(self._serie_delay(serie), axis=1)
        if prefix:
            return dataframe.add_prefix(prefix)
        return dataframe

    def _get_array(self, serie):
        return np.stack(self._serie_delay(serie), axis=1)


    def _serie_delay(self, serie):
        return [serie.shift(delay) for delay in reversed(self.range_delays)]
        
class StackedDataFrameDelay:
    def array3d(self):
        pass
    def array2d(self):
        pass
    def dataframe(self):
        pass