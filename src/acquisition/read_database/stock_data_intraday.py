from functools import reduce
import pandas as pd
from src.database.database import DataBase
from src.read_database.errors.check_stock_data_intraday \
     import CheckErrorsGetStockDataIntraday1minFromDataBase
from src.builder_formats.dataframe import build_dataframe_from_timeseries_dict



class GetStockDataIntraday1minFromDataBase(DataBase):

    DATABASE_NAME = 'stock_data_intraday_1min'

    def __init__(self, format_output='dataframe'):
        super().__init__(name_database=self.DATABASE_NAME)
        self.func_transformer_dataframe = self.__get_function_transformer_dataframe(format_output)
        self.check_errors = CheckErrorsGetStockDataIntraday1minFromDataBase()

    def get(self, stock, start, end, **kwards):

        '''
        This function return stock data from stock_data_intraday_1min data base
        selecting between start and end date.
        Format of output will be the one specified when creating the class.

        Parameters
        -----------
        ---> stock: specify label (name) of stock data.
        ---> start: str or pd.Timedelta,  specify the initial date (including this one).
        ---> end: str or pd.Timedelta,  specify the end date (including this one).
        '''

        dataframe = (
            self.__build_dataframe(
                dict_stock=self.__get_dict_from_database(stock,
                                                         start=self.__get_datetime_database(start),
                                                         end=self.__get_datetime_database(end)),
                start=start,
                end=end,
                **kwards)
        )
        return self.func_transformer_dataframe(dataframe=dataframe, **kwards)

    def __get_dict_from_database(self, stock, start, end):
        return reduce(lambda cum_dict, dict_new: dict(cum_dict, **dict_new),
                      self.database[stock].find(filter={'_id' : {'$gte' : start,
                                                                 '$lte' : end}},
                                                projection={'_id' : 0}))

    def __get_function_transformer_dataframe(self, format_output):
        if format_output == 'dict':
            return self.__get_dict_from_dataframe
        return lambda dataframe, **kwards: dataframe

    @staticmethod
    def __get_datetime_database(date):
        if isinstance(date, pd.Timedelta):
            return pd.to_datetime(date.date())
        return pd.to_datetime(date[:10])

    @staticmethod
    def __build_dataframe(dict_stock, start, end, format_index=None, **kwards):
        return build_dataframe_from_timeseries_dict(dataframe=dict_stock,
                                                    format_index=format_index,
                                                    datetime_index=True,
                                                    ascending=True).loc[start:end]


    @staticmethod
    def __get_dict_from_dataframe(dataframe, orient='index', **kwards):
        dataframe.index = dataframe.index.astype(str)
        return dataframe.to_dict(orient=orient)
