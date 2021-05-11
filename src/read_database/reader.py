from src.database.database import DataBaseAdminDataReader
from src.read_database.errors.check_data import CheckErrorsDataFromDataBase
from src.tools.builder_formats.dataframe import BuildDataFrameFromDB


class ReaderDataBase(DataBaseAdminDataReader):
    '''
    This class is used for reading databases of no-events data.
    '''

    def __init__(self, db_name, format_output):

        self._builder_dataframe = BuildDataFrameFromDB()
        self._db_name = db_name
        super().__init__(db_name)
        self.func_transform_dataframe = self._get_function_transform_dataframe(format_output)
        self.check_errors = CheckErrorsDataFromDataBase()

    @DataBaseAdminDataReader.try_and_wakeup
    def _get_dict_from_database(self, data, start, end, **kwargs):
        return self.database[data].find(filter={'_id' : {'$gte' : start,
                                                         '$lte' : end}},
                                        **kwargs)

    def _get_function_transform_dataframe(self, format_output):
        return self._get_dict_from_dataframe if format_output == 'dict' \
        else lambda dataframe, **kwargs: dataframe

    @staticmethod
    def _get_dict_from_dataframe(dataframe, orient='index', **kwargs):
        dataframe.index = dataframe.index.astype(str)
        return dataframe.to_dict(orient=orient)     

    @classmethod
    def _dataframe(cls, **kwargs):
        return cls(format_output='dataframe', **kwargs)

    @classmethod
    def _dict(cls, **kwargs):
        return cls(format_output='dict', **kwargs)
        

                                          
