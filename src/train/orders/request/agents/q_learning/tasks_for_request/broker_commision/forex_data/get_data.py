from src.read_database.forex_data import ForexDataFromDataBase
import pandas as pd
import numpy as np

class GetDataTask:

    _reader = ForexDataFromDataBase.daily_dataframe()

    def __call__(self, from_symbol, to_symbol, index):

        return self._reindex_and_fill(

            self._reader.get(from_symbol, 
                             to_symbol, 
                             *self._get_limits_from_index(index)), 
            index
        )
    @staticmethod
    def _get_limits_from_index(index):
        return tuple(index[[0,-1]])


    @staticmethod
    def _reindex_and_fill(df, index):
        forex_df = df.asfreq('D').loc[index].ffill().bfill()
        assert np.all(forex_df.index == index)
        
        return forex_df
