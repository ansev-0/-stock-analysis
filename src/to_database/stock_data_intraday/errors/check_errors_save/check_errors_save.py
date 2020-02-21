from src.features_database.features_get.databases_get_features import DataBasesFeatureGet
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveInDataBase(DataBasesFeatureGet):

    parameters = []
    __ID_DOCUMENT = 'general_summary'
    def __init__(self, frecuency):
        super().__init__(self, collection='intraday', document_id=self.__ID_DOCUMENT)
        self.get_features()
        self.__frecuency=frecuency

    @staticmethod
    def check_parameter_create(create):
        if create  not in ['create', 'not create']:
            raise ToDataBaseError('Invalid parameter: if_not_in_base', ValueError)

    def check_frecuency_in_database(self):
        if self.__frecuency not in self.features['frecuency']:
            raise ToDataBaseError('Frecuency not in DataBase', ValueError)
        

