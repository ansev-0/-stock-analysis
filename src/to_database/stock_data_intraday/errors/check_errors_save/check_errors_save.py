from src.to_database.stock_data_intraday.errors.check_errors_intraday import CheckToDataBaseIntraday
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveInDataBase(CheckToDataBaseIntraday):

    parameters = []
    __ID_DOCUMENT = 'general_summary'
    def __init__(self, frecuency):
        super().__init__(self, name='database features')
        self.__frecuency = frecuency
        self.update_supported_parameters()

    @staticmethod
    def check_parameter_create(create):
        if create  not in ['create', 'not create']:
            raise ToDataBaseError('Invalid parameter: if_not_in_base', ValueError)

    def check_frecuency_in_database(self):
        if self.__frecuency not in self.parameters['frecuency']:
            raise ToDataBaseError('Frecuency not in DataBase', ValueError)
        

