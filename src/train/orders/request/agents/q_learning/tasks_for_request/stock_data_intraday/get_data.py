from src.read_database.stock_data import StockDataFromDataBase
import pandas as pd
import numpy as np

class GetDataTask:

    _reader = StockDataFromDataBase.intraday_dataframe('1min')

    def __call__(self, company, index):
        df_intraday = self._reader.get(company, 
                                       *self._get_limits_from_index(index))

        self._check_index(df_intraday.index, index)
        
        return self._prepare_df(
            df_intraday, 
            index
        )

    @staticmethod
    def _check_index(intraday_index, index_init):
       if intraday_index[0] > index_init[0]:
            index_0 = index_init[0]
            raise ValueError (f'No broker data in {index_0}') 

    @staticmethod
    def _get_limits_from_index(index):
        i1, i2 = tuple(index[[0,-1]])
        i1 = i1 - pd.to_timedelta('1W')
        return i1, i2


    @staticmethod
    def _prepare_df(df, index):
        df = df.asfreq('T')
        df = df.fillna(df['close'].ffill()
                                  .to_frame()
                                  .reindex(columns=['open', 'high', 'low', 'close'])
                                  .ffill(axis=1).bfill(axis=1)).ffill()\
                                  .loc[df.index.to_series().dt.date.isin(index.date)]
        return df
