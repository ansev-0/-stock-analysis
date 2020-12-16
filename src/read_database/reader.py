from src.database.database import DataBaseAdminDataReader
from src.read_database.errors.check_data import CheckErrorsDataFromDataBase
from src.tools.builder_formats.dataframe import build_dataframe_from_timeseries_dict


class ReaderDataBase(DataBaseAdminDataReader):
    '''
    This class is used for reading databasesof of no-events data.
    '''

    def __init__(self, db_name, format_output):

        self._db_name = db_name
        super().__init__(db_name)
        self.func_transform_dataframe = self.__get_function_transform_dataframe(format_output)
        self.check_errors = CheckErrorsDataFromDataBase()

    def _get_dict_from_database(self, data, start, end, **kwargs):
        return self.database[data].find(filter={'_id' : {'$gte' : start,
                                                         '$lte' : end}},
                                        **kwargs)

    def __get_function_transform_dataframe(self, format_output):
        if format_output == 'dict':
            return self.__get_dict_from_dataframe
        return lambda dataframe, **kwargs: dataframe

    @staticmethod
    def __get_dict_from_dataframe(dataframe, orient='index', **kwargs):
        dataframe.index = dataframe.index.astype(str)
        return dataframe.to_dict(orient=orient)     
        

    @staticmethod
    def __build_dataframe(dict_data, start, end, format_index=None, **kwargs):
        return build_dataframe_from_timeseries_dict(dataframe=dict_data,
                                                    datetime_index=True,
                                                    format_index=format_index,
                                                    ascending=True).loc[start:end]                                            
