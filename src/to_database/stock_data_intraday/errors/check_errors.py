from src.database.database import DataBase
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveStockDataIntraday:

    __COLLECTION_API_FEATURES = 'intraday'
    def __init__(self, api):
        self.database_api_features = DataBase(name_database='api_features')
        self.api=api


    def check_api_supported(self):
        list_apis=self.__get_apis()
        if self.api not in self.__get_apis():
            raise ToDataBaseError(f'Invalid API: {self.api}, the valid API are: {list_apis}',
                                  ValueError)


    def __get_apis(self):
        collection_intraday=self.database_api_features.database[self.__COLLECTION_API_FEATURES]
        return list(map(lambda x: x['_id'], collection_intraday.find({}, projection='_id')))