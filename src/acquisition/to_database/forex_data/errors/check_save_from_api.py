from src.acquisition.to_database.errors.check_save_from_api import CheckErrorsSaveFromApi
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveForexDataFromApi(CheckErrorsSaveFromApi):


    @staticmethod
    def check_list_tuples(list_queries):
        if not isinstance(list_queries, list):
            raise ToDataBaseError('You must pass a list', TypeError)

        if not all(map(lambda query: isinstance(query, tuple),
                       list_queries)
                  ):
            raise ToDataBaseError('You must pass a list of tuples', TypeError)


     
    @classmethod
    def intraday(cls, api): 
        return cls(api=api, collection='intraday')

    @classmethod
    def daily_adjusted(cls, api): 
        return cls(api=api, collection='daily_adjusted')
        
        