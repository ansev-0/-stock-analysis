from src.database.database import DataBase
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveFromApi:

    def __init__(self, api, collection):
        self.__database = DataBase()
        self.__database.connect(database_name='api_features')
        self.database_api_features = self.__database.database
        self.api = api
        self.collection = collection

    def check_api_supported(self):
        list_apis=self.__get_apis()
        if self.api not in list_apis:
            raise ToDataBaseError(f'Invalid API: {self.api}, the valid API are: {list_apis}',
                                  ValueError)
    def __get_apis(self):
        collection_intraday = self.database_api_features[self.collection]
        return list(map(lambda x: x['_id'], collection_intraday.find({}, projection='_id')))
