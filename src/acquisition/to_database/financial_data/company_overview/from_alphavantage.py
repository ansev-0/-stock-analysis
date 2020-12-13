from src.acquisition.to_database.financial_data.company_overview.update_overview_database import UpdateOverview
from src.acquisition.acquisition.alphavantage.fundamental_data import FundamentalData
from src.acquisition.to_database.save_many_stock_collection import SaveMany



class UpdateOverviewAlphaVantage(UpdateOverview):
    '''
    This class is an interface to save the OVERVIEW data of the Alphavantage API

    Parameters
    ----------

    apikey: str.
        key of API Alphavantage.

    new_database: str
        valid parameters = 'create' and 'not create'

    '''
    def __init__(self, apikey, new_database='create', **kwargs):
        #Create connection to the database
        super().__init__(new_database=new_database)
        # Create reader from AlphaVantage
        self.__reader = FundamentalData(apikey=apikey, **kwargs)

    def to_database(self, company):
        '''
        This function save in DataBase the data of the specified company,
        when an API error is obtained, the error returns,
        if no error is obtained, nothing returns (None)
        '''
        #Get response from reader Api Alphavantage
        response = self.__read_from_alphavantage(company=company)

        if isinstance(response, tuple):
            return response

        # response is test  in AlphaVantage.__read() by:
        #acquistion.errors_response.ErrorsResponseApiAlphavantage().

        #Update collection
        #Get correct format
        list_dicts_to_update = self._to_valid_format(response)
        #Call to update
        self.update(company=company, dict_to_update=list_dicts_to_update)

        return None


    def _to_valid_format(self, data):
        # rename 
        return {key if key != 'LatestQuarter' else '_id' : value 
                for key, value in data.items()}

    def __read_from_alphavantage(self, company):
        '''
        This function gets the API response,
        returns a dictionary if the answer does not contain errors,
        and a list if there are errors.
        '''
        return self.__reader.get_overview(symbol=company)




class UpdateOverviewAlphaVantageMany(UpdateOverviewAlphaVantage):

    __save_many=SaveMany()
    
    def to_database_getting_errors(self, list_company):
        return self.__save_many.save_and_return_errors(self.to_database, list_company)

    def to_database_ignoring_errors(self, list_company):
        return self.__save_many.save(self.to_database, list_company)
        
