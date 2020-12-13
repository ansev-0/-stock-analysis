from src.acquisition.to_database.errors.check_save_from_api import CheckErrorsSaveFromApi
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveFinancialDataFromApi(CheckErrorsSaveFromApi):


    @staticmethod
    def check_list_queries(list_queries):
        if not isinstance(list_queries, (list, tuple)):
            raise ToDataBaseError('You must pass a list of stocks names', TypeError)
    
    @classmethod
    def overview(cls, api): 
        return cls(api=api, collection='overview')

    @classmethod
    def balance_sheet(cls, api): 
        return cls(api=api, collection='balance_sheet')

    @classmethod
    def cash_flow(cls, api): 
        return cls(api=api, collection='cash_flow')

    @classmethod
    def earnings(cls, api): 
        return cls(api=api, collection='earnings')

    @classmethod
    def income_statement(cls, api): 
        return cls(api=api, collection='income_statement')
        
        