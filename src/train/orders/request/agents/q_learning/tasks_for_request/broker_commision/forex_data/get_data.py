from src.read_database.forex_data import ForexDataFromDataBase
import pandas as pd
import numpy as np

class GetDataTask:

    _reader = ForexDataFromDataBase.daily_dataframe()

    def __call__(self, from_symbol, to_symbol, index):
        df_broker = self._reader.get(from_symbol, 
                             to_symbol, 
                             *self._get_limits_from_index(index))

        self._check_index(df_broker.index, index)
        
        return self._reindex_and_fill(

            df_broker, 
            index
        )

    @staticmethod
    def _check_index(broker_index, index_init):
       if broker_index[0] > index_init[0]:
            index_0 = index_init[0]
            raise ValueError (f'No broker data in {index_0}') 

    @staticmethod
    def _get_limits_from_index(index):
        i1, i2 = tuple(index[[0,-1]])
        i1 = i1 - pd.to_timedelta('4W')
        return i1, i2


    @staticmethod
    def _reindex_and_fill(df, index):
        # fix it
        forex_df = df.asfreq('D').ffill().loc[index]
        assert np.all(forex_df.index == index)
        
        return forex_df
