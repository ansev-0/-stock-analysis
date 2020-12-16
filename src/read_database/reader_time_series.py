from src.read_database.reader import ReaderDataBase
from src.tools.builder_formats.dataframe import build_dataframe_from_timeseries_dict
from src.tools.mappers import map_dict_from_underscore
from src.tools.reduce_tools import combine_dicts
import pandas as pd

class TimeSeriesDataFromDataBase(ReaderDataBase):
    '''
    This class is used for reading time series databases.
    '''

    def __init__(self, db_name, format_output='dataframe'):

        super().__init__(db_name)
        self.func_transform_dataframe = self.__get_function_transform_dataframe(format_output)
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
        dict_data = self._get_dict_from_database(collection,
                                                 start=self.__get_datetime_database(start),
                                                 end=self.__get_datetime_database(end),
                                                 projection={'_id' : 0})
        if dict_data:
            dataframe = (
                self.__build_dataframe(dict_data=dict_data, start=start, end=end, **kwargs))
            return self.func_transform_dataframe(dataframe=dataframe, **kwargs)
        return dict_data

    def _get_dict_from_database(self, data, start, end, **kwargs):
        try:
            return combine_dicts(*super()._get_dict_from_database(data, start, end, **kwargs))

        except TypeError:
            return None

    def __get_datetime_database(self, date):
        return self.datetime_index.get(date, self._db_name)


class DateTimeIndexDataBase:
    __MAPPER_CUT_DATE = {'intraday' : lambda date: date.date(),
                         'daily' : lambda date: str(date)[:7]}

    def get(self, date, db_name):
        if  not isinstance(date, pd.Timedelta):
            date = pd.to_datetime(date)
        date = pd.to_datetime(map_dict_from_underscore(
            self.__MAPPER_CUT_DATE, db_name, 2, default_key=None)(date))
        return date
