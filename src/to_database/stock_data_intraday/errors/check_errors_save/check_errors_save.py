from src.to_database.stock_data_intraday.errors.check_errors_intraday import CheckToDataBaseIntraday
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveInDataBase(CheckToDataBaseIntraday):

    parameters = []
    __ID_DOCUMENT = 'status_summary'

    def __init__(self):
        super().__init__(self, name='database features')
        self.update_supported_parameters()

    @staticmethod
    def check_parameter_create(create):
        if create  not in ['create', 'not create']:
            raise ToDataBaseError('Invalid parameter: if_not_in_base', ValueError)

    def check_frecuency_in_database(self, frecuency):
        if frecuency not in self.parameters['frecuency']:
            raise ToDataBaseError('Frecuency not in DataBase', ValueError)
        

