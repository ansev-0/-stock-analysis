from functools import reduce
import pandas as pd
from src.database.database import DataBaseAdminDataReader
from src.read_database.errors.check_data import CheckErrorsDataFromDataBase
from src.tools.builder_formats.dataframe import build_dataframe_from_timeseries_dict
from src.tools.mappers import map_dict_from_underscore
from src.exceptions.readbase_exceptions import GetFromDataBaseError


class DataFromDataBase(DataBaseAdminDataReader):
    '''
    This class is used for reading databases.
    '''

    def __init__(self, db_name, format_output='dataframe'):
        self._db_name = db_name

        super().__init__(db_name)
        self.func_transform_dataframe = self.__get_function_transform_dataframe(format_output)
        self.check_errors = CheckErrorsDataFromDataBase()
        self.datetime_index = DateTimeIndexDataBase()

    @property
    def data_names(self):
        return self.database.collection_names()


    def get(self, collection, start, end, **kwargs):

        '''

        This function get data data from data data base between two dates:
        start and end (both inclusive).

        Parameters
        --------------
        collection: label(name)
        start: str or pd.Timedelta.
        end str or pd.Timedelta.

        '''
        dict_data = self.__get_dict_from_database(collection,
                                                   start=self.__get_datetime_database(start),
                                                   end=self.__get_datetime_database(end))
        if dict_data:
            dataframe = (
                self.__build_dataframe(dict_data=dict_data, start=start, end=end, **kwargs))
            return self.func_transform_dataframe(dataframe=dataframe, **kwargs)
        return dict_data

    def __get_dict_from_database(self, data, start, end):
        try:
            return reduce(lambda cum_dict, dict_new: dict(cum_dict, **dict_new),
                          self.database[data].find(filter={'_id' : {'$gte' : start,
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
    def __build_dataframe(dict_data, start, end, format_index=None, **kwargs):
        return build_dataframe_from_timeseries_dict(dataframe=dict_data,
                                                    datetime_index=True,
                                                    format_index=format_index,
                                                    ascending=True).loc[start:end]

    @staticmethod
    def __get_dict_from_dataframe(dataframe, orient='index', **kwargs):
        dataframe.index = dataframe.index.astype(str)
        return dataframe.to_dict(orient=orient)



class DateTimeIndexDataBase:
    __MAPPER_CUT_DATE = {'intraday' : lambda date: date.date(),
                         'daily' : lambda date: str(date)[:7]}

    def get(self, date, db_name):
        if  not isinstance(date, pd.Timedelta):
            date = pd.to_datetime(date)
        date = pd.to_datetime(map_dict_from_underscore(
            self.__MAPPER_CUT_DATE, db_name, 2, default_key=None)(date))
        return date



