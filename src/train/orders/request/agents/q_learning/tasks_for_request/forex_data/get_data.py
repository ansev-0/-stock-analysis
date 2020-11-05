from src.read_database.forex_data import ForexDataFromDataBase
import pandas as pd


class GetDataTask:

    _reader = ForexDataFromDataBase.daily_dataframe()

    def __call__(self, from_symbol, to_symbol, index_train, index_val):

        return tuple(
            map(
                lambda index: self._reindex_and_fill(
                    self._reader.get(from_symbol, 
                                     to_symbol, 
                                     *self._get_limits_from_index(index)), 
                    index),
                (index_train, index_val))
                    )

    @staticmethod
    def _get_limits_from_index(index):
        return tuple(index[[0,-1]])


    @staticmethod
    def _reindex_and_fill(df, index):
        return df.asfreq('D').loc[index].ffill()
