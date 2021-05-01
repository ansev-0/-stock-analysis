from src.exceptions.readbase_exceptions import GetFromDataBaseError
from src.read_database.reader_time_series import TimeSeriesDataFromDataBase


class StockDataFromDataBase(TimeSeriesDataFromDataBase):
    '''
    This class is used for reading stock_data databases.
    '''

    @classmethod
    def intraday_dataframe(cls, freq):
        return cls._dataframe(db_name=f'stock_data_intraday_{freq}')

    @classmethod
    def dailyadj_dataframe(cls):
        return cls._dataframe(db_name='stock_data_daily_adjusted')

    @classmethod
    def intraday_dict(cls, freq):
        return cls._dict(db_name=f'stock_data_intraday_{freq}')

    @classmethod
    def dailyadj_dict(cls):
        return cls._dict(db_name='stock_data_daily_adjusted')


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
    

