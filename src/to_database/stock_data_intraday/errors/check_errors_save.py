from src.to_database.stock_data_intraday.errors.check_errors_intraday import CheckToDataBaseIntraday
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveInDataBase(CheckToDataBaseIntraday):

    frecuencies_intraday_in_database = []
    __ID_DOCUMENT = 'database'

    def __init__(self):
        super().__init__()
        self.frecuencies_intraday_in_database = self.__get_supported_frequencies(document_id=self.__ID_DOCUMENT)

    def check_parameter_create(self, create):
        if create  not in ['create', 'not create']:
            raise ToDataBaseError('Invalid parameter: if_not_in_base', ValueError)

    def check_frecuency_in_database(self, frecuency):
        if not self.__frecuency_supported(frecuency=frecuency, 
                                          list_frecuencies=self.frecuencies_intraday_in_database):
            raise ToDataBaseError('Frecuency not in DataBase', ValueError)
        