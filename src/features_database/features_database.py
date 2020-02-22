from src.database.database import DataBase

class FeaturesDataBase(DataBase):
    __SUPPORTED_DATABASE = ['database_features', 'api_features']

    def __init__(self, name_database, collection, document_id):
        self.check_supported(name_database)
        super().__init__(name_database=name_database)
        self._collection = self.database[collection]
        self._document_id = document_id

    def check_supported(self, name):
        if name not in self.__SUPPORTED_DATABASE:
            raise ValueError(f'the databases supported by this class are:\
                             {self.__SUPPORTED_DATABASE}')
