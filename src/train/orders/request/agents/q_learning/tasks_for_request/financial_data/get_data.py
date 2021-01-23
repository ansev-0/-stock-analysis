from src.read_database.financial_data.reader_many_financial_features import ManyFinancialFeaturesFromDataBase
import pandas as pd

class GetDataTask:

    _reader = ManyFinancialFeaturesFromDataBase()

    def __call__(self, symbol, index):
        financial_df = self._reader.get(symbol, 
                                        *self._get_limits_from_index(index))
        if financial_df.index[0] > index[0]:
            index_0 = index[0]
            raise ValueError (f'No financial data in {index_0}')
        return financial_df
   
    @staticmethod
    def _get_limits_from_index(index):
        return tuple(index[[0,-1]])




