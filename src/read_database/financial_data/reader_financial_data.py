from src.read_database.reader import ReaderDataBase
from src.tools.builder_formats.dataframe import build_dataframe_from_timeseries_dict
from src.tools.reduce_tools import combine_dicts
import pandas as pd

class FinancialDataFromDataBase(ReaderDataBase):
    '''
    This class is used for reading time series databases.
    '''

    def __init__(self, db_name, format_output='dataframe'):

        super().__init__(db_name, format_output)

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
                                                 start=self.__get_datetime_index(start),
                                                 end=self.__get_datetime_index(end),
                                                )
        if dict_data:
            dataframe = (
                self.__build_dataframe(dict_data=dict_data, start=start, end=end, **kwargs))
            return self.func_transform_dataframe(dataframe=dataframe, **kwargs)
        return dict_data

        
    def _get_dict_from_database(self, data, start, end, **kwargs):
        consult_result = super()._get_dict_from_database(data, start, end, **kwargs)
        try:
            return combine_dicts(*[{d['_id'] : {key : value for key, value in d.items() 
                                                if key != '_id'}} 
                                    for d in consult_result])

        except TypeError:
            return None

    @staticmethod
    def __get_datetime_index(value):
        if isinstance(value, str):
            return pd.to_datetime(value)
        return value

#reader = FinancialDataFromDataBase('balance_sheet_quarterly')
#output = reader.get('IBM', '01/01/2019', '09/12/2020')
#pass
#print(output)