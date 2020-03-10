from src.database.database import DataBase

class FeaturesDataBase:
    __SUPPORTED_DATABASE = ['database_features', 'api_features']

    def __init__(self, database_name, collection, document_id):
        self.check_supported(database_name)
        self.__database = DataBase()
        self.__database.connect(database_name)
        self._collection = self.__database.database[collection]
        self._document_id = document_id

    def check_supported(self, name):
        if name not in self.__SUPPORTED_DATABASE:
            raise ValueError(f'the databases supported by this class are:\
                             {self.__SUPPORTED_DATABASE}')

    @classmethod
    def databases(cls, collection, document_id):
        return cls(database_name='database_features',
                   collection=collection,
                   document_id=document_id)

    @classmethod
    def api_alphavantage(cls, collection):
        return cls(database_name='api_features',
                   collection=collection,
                   document_id='alphavantage')
                   