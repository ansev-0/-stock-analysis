from functools import reduce
import pandas as pd
from src.database.database import DataBaseAdminDataReader
from src.read_database.errors.check_stock_data import CheckErrorsStockDataFromDataBase
from src.tools.builder_formats.dataframe import build_dataframe_from_timeseries_dict
from src.tools.mappers import map_dict_from_underscore
from src.exceptions.readbase_exceptions import GetFromDataBaseError


class StockDataFromDataBase(DataBaseAdminDataReader):
    '''
    This class is used for reading stock_data databases.
    '''

    def __init__(self, db_name, format_output='dataframe'):
        self._db_name = db_name

        super().__init__(db_name)
        self.func_transform_dataframe = self.__get_function_transform_dataframe(format_output)
        self.check_errors = CheckErrorsStockDataFromDataBase()
        self.datetime_index = DateTimeIndexDataBase()

    @property
    def stock_names(self):
        return self.database.collection_names()


    def get(self, stock, start, end, **kwargs):

        '''

        This function get stock data from stock data base between two dates:
        start and end (both inclusive).

        Parameters
        --------------
        stock: label(name) of stock data.
        start: str or pd.Timedelta.
        end str or pd.Timedelta.

        '''
        dict_stock = self.__get_dict_from_database(stock,
                                                   start=self.__get_datetime_database(start),
                                                   end=self.__get_datetime_database(end))
        if dict_stock:
            dataframe = (
                self.__build_dataframe(dict_stock=dict_stock, start=start, end=end, **kwargs))
            return self.func_transform_dataframe(dataframe=dataframe, **kwargs)
        return dict_stock

    def __get_dict_from_database(self, stock, start, end):
        try:
            return reduce(lambda cum_dict, dict_new: dict(cum_dict, **dict_new),
                          self.database[stock].find(filter={'_id' : {'$gte' : start,
                                                                     '$lte' : end}},
                                                            projection={'_id' : 0}))
        except TypeError:
            return None

    def __get_function_transform_dataframe(self, format_output):
        if format_output == 'dict':
            return self.__get_dict_from_dataframe
        return lambda dataframe, **kwargs: dataframe

    

    
    def __get_datetime_database(self, date):
        return self.datetime_index.get(date, self._db_name)

    @staticmethod
    def __build_dataframe(dict_stock, start, end, format_index=None, **kwargs):
        return build_dataframe_from_timeseries_dict(dataframe=dict_stock,
                                                    datetime_index=True,
                                                    format_index=format_index,
                                                    ascending=True).loc[start:end]

    @staticmethod
    def __get_dict_from_dataframe(dataframe, orient='index', **kwargs):
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
    def __dataframe(cls, **kwargs):
        return cls(format_output='dataframe', **kwargs)

    @classmethod
    def __dict(cls, **kwargs):
        return cls(format_output='dict', **kwargs)



class DateTimeIndexDataBase:
    __MAPPER_CUT_DATE = {'intraday' : lambda date: date.date(),
                         'daily' : lambda date: str(date)[:7]}

    def get(self, date, db_name):
        if  not isinstance(date, pd.Timedelta):
            date = pd.to_datetime(date)
        date = pd.to_datetime(map_dict_from_underscore(
            self.__MAPPER_CUT_DATE, db_name, 2, default_key=None)(date))
        return date



class ManyStockDataFromDataBase(StockDataFromDataBase):

    def get_fixed_dates(self, stock_labels, start, end, **kwargs):
        return map(lambda stock: self.get(stock=stock, start=start, end=end, **kwargs),
                   stock_labels)
    
    def get_from_dict(self, list_kparams, **kwargs):
        return map(lambda kparams: self.get(**kparams, **kwargs),
                   list_kparams)

    def get_many(self, list_params, **kwargs):
        return map(lambda args: self.get(*args, **kwargs),
                   list_params)

class ManyStockDataFromManyDataBase:

    def __init__(self, db_names, format_output='dataframe'):
        self._db_names = db_names
        self._readers = self.__create_readers(db_names, format_output)


    def get_fixed_dates(self, db_stock_dict, start, end, **kwargs):

        return self.__get(lambda reader, params, *args, **kwargs : \
                          reader.get_fixed_dates(params, *args, **kwargs),
                          db_stock_dict,
                          start,
                          end,
                          **kwargs)


    def get_from_dict(self, dict_list_kparams, **kwargs):
        return self.__get(lambda reader, params, **kwargs : \
                          reader.get_from_dict(params, **kwargs),
                          dict_list_kparams,
                          **kwargs)
            

    def get_many(self, dict_list_params, **kwargs):
        return self.__get(lambda reader, params, **kwargs : \
                          reader.get_many(params, **kwargs),
                          dict_list_params,
                          **kwargs)

    def __create_readers(self, database_names, format_output):
            return {db_name : ManyStockDataFromDataBase(db_name, format_output=format_output) 
                    for db_name in database_names}
    
    def __get(self, function, dict_params_by_database, *args, **kwargs):
        response_dict = {}
        for db_name, params in dict_params_by_database.items():
            try:
                response_dict[db_name] = function(self._readers[db_name], params, *args, **kwargs)
            except KeyError:
                raise GetFromDataBaseError(f'Database not supported, databases supported : {self._db_names}',
                                           KeyError)
        return response_dict

    @classmethod
    def frame(cls, db_names):
        return cls(db_names, format_output='dataframe')

    @classmethod
    def dictionary(cls, db_names):
        return cls(db_names, format_output='dict')
    
