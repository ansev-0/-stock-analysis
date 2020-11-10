from src.train.database.cache.agents.find import FindAgentTrainCache
import pandas as pd
import numpy as np

class TimeStatesValues:

    def __init__(self, cache_id=None, time_data=None):

        self._cache_id = cache_id
        self._time_values = self._init_time_values(time_data)
        self._time_values_diff = np.concatenate(([np.nan], np.diff(self._time_values)))
        self._time_values_done = self._get_values_done()

    def __len__(self):
        return len(self._time_values)

    def __call__(self, index):
        return self._time_values[index], self._time_values_diff[index], self._time_values_done[index]

    def incr(self, index):
        return self._time_values_diff[index]
        
    def value(self, index):
        return self._time_values[index]

    def done(self, index):
        return self._time_values_done[index]

    def _init_time_values(self, time_data):
        if self._cache_id is not None:
            return self._time_values_from_cache()
        elif time_data is not None:
            return self._time_values_input(time_data)

        raise ValueError('You must pass time_series or cache_id parameters')

    def _time_values_input(self, time_data):

        if isinstance(time_data, np.ndarray):
            return time_data
        elif isinstance(time_data, pd.Series):
            return time_data.to_numpy()
        else:
            return np.array(time_data)

    def _time_values_from_cache(self):
        return np.array(
            tuple(
                FindAgentTrainCache().\
            find_by_id(self._cache_id, 
                       projection = {'time_values' : True,
                                     '_id' : False})['time_values'].values()
                )[:-1]
        )

    def _get_values_done(self):
        value_serie = pd.Series(self._time_values)
        return (value_serie.lt(value_serie.shift())
            & value_serie.lt(value_serie.shift(-1))).to_numpy()
