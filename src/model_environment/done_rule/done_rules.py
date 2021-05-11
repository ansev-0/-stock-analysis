import pandas as pd
import numpy as np

class DoneRules:

    def never(self, time_values):
        return np.array([False]*len(time_values))

    def local_min_or_max(self, time_values):
        
        time_values = self._data_time_serie(time_values)
        return (self._local_min_serie(time_values) | 
                self._local_max_serie(time_values)).to_numpy()

    def one_before_local_min_or_max(self, time_values):
        time_values = self._data_time_serie(time_values)
        return (self._local_min_serie(time_values) | 
                self._local_max_serie(time_values)).shift(-1, fill_value=False).to_numpy()

    def local_min(self, time_values):

        time_values = self._data_time_serie(time_values)
        return self._local_min_serie(time_values).to_numpy()

    def one_before_local_min(self, time_values):
        time_values = self._data_time_serie(time_values)
        return self._local_min_serie(time_values).shift(-1, fill_value=False).to_numpy()

    def local_max(self, time_values):

        time_values = self._data_time_serie(time_values)
        return self._local_max_serie(time_values).to_numpy()

    def one_before_local_max(self, time_values):
        time_values = self._data_time_serie(time_values)
        return self._local_max_serie(time_values).shift(-1, fill_value=False).to_numpy()

    @staticmethod
    def _local_min_serie(time_serie):
        return time_serie.lt(time_serie.shift()) & time_serie.lt(time_serie.shift(-1))

    @staticmethod
    def _local_max_serie(time_serie):
        return time_serie.gt(time_serie.shift()) & time_serie.gt(time_serie.shift(-1))

    @staticmethod
    def _data_time_serie(data):
        return pd.Series(data) if not isinstance(data, pd.Series) else data
