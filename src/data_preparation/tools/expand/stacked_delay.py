import pandas as pd
import numpy as np
from functools import wraps

class StackedSequences:

    def __init__(self, range_delays):
        self.range_delays = range_delays

    @property
    def range_delays(self):
        return self._range_delays

    @range_delays.setter
    def range_delays(self, range_delays):
        self._range_delays = range_delays
        self._reversed_delays = tuple(reversed(self._range_delays))
    
    def array(self, shiftable):
        return np.stack(self._create_list_from_delays(shiftable), axis=1)

    def concat_dataframe(self, shiftable):
        return pd.concat(self._create_list_from_delays(shiftable), axis=1, sort=False)

    def remove_rows_with_nan(self, array):
        return array[self.range_delays.stop-1:]


    def _create_list_from_delays(self, shiftable):
        return [shiftable.shift(delay) for delay in self._reversed_delays]



class StackedSequencesFromSeries(StackedSequences):

    def dataframe(self, serie):
        dataframe = self.concat_dataframe(serie)


        return dataframe.set_axis([f'{name}_{delay}' for name, delay in 
                                   zip(dataframe.columns, self._reversed_delays)], axis=1)

    def dataframe_without_nan(self, serie):
        return self.dataframe(serie).dropna()
    
    def array_without_nan(self, serie):
        return  self.remove_rows_with_nan(self.array(serie))

    def array3d(self, serie):
        return np.expand_dims(self.array(serie), 2)
        
    def array3d_without_nan(self, serie):
        return np.expand_dims(self.array_without_nan(serie), 2)

class StackedSequencesFromDataFrame(StackedSequences):
    
    def dataframe(self, dataframe):
        n_features = len(dataframe.columns)
        dataframe = self.concat_dataframe(dataframe)
        return dataframe.set_axis(self._get_multiindex(dataframe.columns, n_features),
                                  axis=1).sort_index(axis=1, ascending=[True, False])

    def array_without_nan(self, dataframe):
        return self.remove_rows_with_nan(self.array(dataframe))


    def dataframe_without_nan(self, dataframe):
        return self.dataframe(dataframe).dropna()

    def _get_multiindex(self, dataframe_columns, n_cols):
        return pd.MultiIndex.from_tuples(zip(dataframe_columns,
                                         np.repeat(self._reversed_delays, n_cols)))


class StackAndMapSequencesFromDataFrame:

    def __init__(self, delays):
        self.delays = delays

    @classmethod
    def wrapper_array(cls, function):

        @wraps(function)
        def map_array(self, dataframe, *args, **kwargs):
            array = dataframe.to_numpy()
            return np.stack([function(array[i : i + self.delays, :], *args, **kwargs) 
                             for i in range(dataframe.shape[0] - self.delays)],
                            axis=2)
        return map_array

    def array(self, dataframe):
        array = dataframe.to_numpy()
        return np.stack([array[i : i + self.delays, :] 
                         for i in range(dataframe.shape[0] - self.delays)],
                          axis=2)


    


