from src.database.database import DataBase
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveStockDataIntraday:

    __COLLECTION_API_FEATURES = 'intraday'
    __REQUIRED_METHODS = ['to_database_getting_errors', 'to_database_ignoring_errors']
    def __init__(self, api):
        self.database_api_features = DataBase(name_database='api_features')
        self.api=api


    def check_api_supported(self):
        list_apis=self.__get_apis()
        if self.api not in self.__get_apis():
            raise ToDataBaseError(f'Invalid API: {self.api}, the valid API are: {list_apis}',
                                  ValueError)

    def check_methods_supported(self, class_save):
        for method in self.__REQUIRED_METHODS:
            try:
                getattr(class_save, method)
            except AttributeError as error:
                raise ToDataBaseError(f'Invalid class, the class must have: {self.__REQUIRED_METHODS} methods', error)


    def check_list_stocks_name(self, list_stock_name):
        if not isinstance(list_stock_name, list):
            return ToDataBaseError('You must pass a list of stocks names', TypeError)


    def __get_apis(self):
        collection_intraday=self.database_api_features.database[self.__COLLECTION_API_FEATURES]
        return list(map(lambda x: x['_id'], collection_intraday.find({}, projection='_id')))