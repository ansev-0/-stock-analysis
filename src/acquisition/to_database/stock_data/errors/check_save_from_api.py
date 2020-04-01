from src.acquisition.to_database.errors.check_save_from_api import CheckErrorsSaveFromApi
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveStockDataFromApi(CheckErrorsSaveFromApi):

    REQUIRED_METHODS = ['to_database_getting_errors', 'to_database_ignoring_errors']
    
    def check_methods_supported(self, object_save):
        for method in self.REQUIRED_METHODS:
            if not hasattr(object_save, method):
                raise ToDataBaseError(f'Invalid class, the class must have:\
                                      {self.REQUIRED_METHODS} methods',
                                      AttributeError)
                                      
    @staticmethod
    def check_list_stocks_name(list_stock_name):
        if not isinstance(list_stock_name, list):
            raise ToDataBaseError('You must pass a list of stocks names', TypeError)

    
    @classmethod
    def intraday(cls, api): 
        return cls(api=api, collection='intraday')

    @classmethod
    def daily_adjusted(cls, api): 
        return cls(api=api, collection='daily_adjusted')
        
        