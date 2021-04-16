from src.read_database.financial_data.reader_many_financial_features import ManyFinancialFeaturesFromDataBase
import pandas as pd

import pandas as pd

class GetDataTask:

    _reader = ManyFinancialFeaturesFromDataBase()

    def __call__(self, symbol, index):

        #index_init = index.copy()
        financial_df = self._make_request_db(symbol, index)
        self._check_index(financial_df.index, index)

        return financial_df

        
    def _make_request_db(self, symbol, index):
        return self._reader.get(symbol, 
                                *self._get_limits_from_index(index))
   
    @staticmethod
    def _get_limits_from_index(index):
        i1, i2 = tuple(index[[0,-1]])
        i1 = i1 - pd.to_timedelta('1Y')
        return i1, i2
        
    @staticmethod
    def _check_index(financial_index, index_init):
       if financial_index[0] > index_init[0]:
            index_0 = index_init[0]
            raise ValueError (f'No financial data in {index_0}') 

    @staticmethod
    def _reindex_and_fill(df, index):
        # fix it
        forex_df = df.asfreq('D').ffill().loc[index]
        assert np.all(forex_df.index == index)
        
        return forex_df





