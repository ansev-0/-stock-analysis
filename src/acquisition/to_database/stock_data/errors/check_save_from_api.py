from src.acquisition.to_database.errors.check_save_from_api import CheckErrorsSaveFromApi
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveStockDataFromApi(CheckErrorsSaveFromApi):


    @staticmethod
    def check_list_queries(list_queries):
        if not isinstance(list_queries, (list, tuple)):
            raise ToDataBaseError('You must pass a list of stocks names', TypeError)
    
    @classmethod
    def intraday(cls, api): 
        return cls(api=api, collection='intraday')

    @classmethod
    def daily_adjusted(cls, api): 
        return cls(api=api, collection='daily_adjusted')
        
        