from src.database.database import DataBase
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveStockDataIntraday:

    COLLECTION_API_FEATURES = 'intraday'
    REQUIRED_METHODS = ['to_database_getting_errors', 'to_database_ignoring_errors']

    def __init__(self, api):
        self.__database = DataBase()
        self.__database.connect(database_name='api_features')
        self.database_api_features = self.__database.database
        self.api=api
        

    def check_api_supported(self):
        list_apis=self.__get_apis()
        if self.api not in self.__get_apis():
            raise ToDataBaseError(f'Invalid API: {self.api}, the valid API are: {list_apis}',
                                  ValueError)

    def check_methods_supported(self, class_save):
        for method in self.REQUIRED_METHODS:
            try:
                getattr(class_save, method)
            except AttributeError as error:
                raise ToDataBaseError(f'Invalid class, the class must have:\
                                      {self.REQUIRED_METHODS} methods',
                                      error)
                                      
    @staticmethod
    def check_list_stocks_name(list_stock_name):
        if not isinstance(list_stock_name, list):
            raise ToDataBaseError('You must pass a list of stocks names', TypeError)

    def __get_apis(self):
        collection_intraday = self.database_api_features[self.COLLECTION_API_FEATURES]
        return list(map(lambda x: x['_id'], collection_intraday.find({}, projection='_id')))
        