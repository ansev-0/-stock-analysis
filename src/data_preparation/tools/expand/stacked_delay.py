import pandas as pd
import numpy as np


class StackedDelay:

    def __init__(self, range_delays):
        self.range_delays = range_delays
        self._reversed_delays = tuple(reversed(self.range_delays))

    
    def array(self, shiftable):
        return np.stack(self._create_list_from_delays(shiftable), axis=1)

    def concat_dataframe(self, shiftable):
        return pd.concat(self._create_list_from_delays(shiftable), axis=1)

    def remove_rows_with_nan(self, array):
        return array[self.range_delays.stop-1:]


    def _create_list_from_delays(self, shiftable):
        return [shiftable.shift(delay) for delay in self._reversed_delays]



class StackedSerieDelay(StackedDelay):

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

class StackedDataFrameDelay(StackedDelay):
    
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

