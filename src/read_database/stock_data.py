from functools import reduce
import pandas as pd
from src.database.database import DataBase
from src.read_database.errors.check_stock_data import CheckErrorsGetStockDataFromDataBase
from src.builder_formats.dataframe import build_dataframe_from_timeseries_dict
from pymongo import MongoClient


class GetStockDataFromDataBase:
    '''

    This class is used for reading stock_data databases.

    '''

    DATABASE_NAME = 'stock_data_daily_adjusted'
    def __init__(self, db_name, format_output='dataframe'):
        self.__db_name = db_name
        self.__database = DataBase()
        self.__database.connect(self.__db_name)
        self.func_transform_dataframe = self.__get_function_transform_dataframe(format_output)
        self.check_errors = CheckErrorsGetStockDataFromDataBase()



    def get(self, stock, start, end, **kwards):

        '''

        This function get stock data from stock_data_intraday_1min data base between two dates:
        start and end (both inclusive).

        Parameters
        --------------
        stock: label(name) of stock data.
        start: str or pd.Timedelta.
        end str or pd.Timedelta.

        '''

        dataframe = (
            self.__build_dataframe(
                dict_stock=self.__get_dict_from_database(stock,
                                                         start=self.__get_datetime_database(start),
                                                         end=self.__get_datetime_database(end)),
                start=start,
                end=end,
                **kwards))
        return self.func_transform_dataframe(dataframe=dataframe, **kwards)

    def __get_dict_from_database(self, stock, start, end):
        return reduce(lambda cum_dict, dict_new: dict(cum_dict, **dict_new),
                      self.__database.database[stock].find(filter={'_id' : {'$gte' : start,
                                                                          '$lte' : end}},
                                                         projection={'_id' : 0}))

    def __get_function_transform_dataframe(self, format_output):
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
                                                    datetime_index=True,
                                                    format_index=format_index,
                                                    ascending=True).loc[start:end]

    @staticmethod
    def __get_dict_from_dataframe(dataframe, orient='index', **kwards):
        dataframe.index = dataframe.index.astype(str)
        return dataframe.to_dict(orient=orient)


    @classmethod
    def intraday_dataframe(cls, freq):
        return cls.__dataframe(db_name=f'stock_data_intraday_{freq}')

    @classmethod
    def dailyadj_dataframe(cls):
        return cls.__dataframe(db_name='stock_data_daily_adjusted')

    @classmethod
    def intraday_dict(cls, freq):
        return cls.__dict(db_name=f'stock_data_intraday_{freq}')

    @classmethod
    def dailyadj_dict(cls):
        return cls.__dict(db_name='stock_data_daily_adjusted')


    @classmethod
    def __dataframe(cls, **kwards):
        return cls(format_output='dataframe', **kwards)

    @classmethod
    def __dict(cls, **kwards):
        return cls(format_output='dict', **kwards)
