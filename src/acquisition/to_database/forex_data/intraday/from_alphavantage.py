from src.acquisition.to_database.forex_data.intraday.update_intraday import UpdateIntraday
from src.acquisition.acquisition.alphavantage.forex import Forex
from src.acquisition.to_database.tools.to_database import CreateDictsWithSameId
from src.acquisition.to_database.forex_data.save_many import SaveMany

class UpdateIntradayAlphavantage(UpdateIntraday):

    '''
    This class is an interface to save the daily forex data of the Alphavantage API

    Parameters
    ----------

    frecuency: str.
        frequency of the data to read,
        it must be supported by the API, consult:
        https://www.alphavantage.co/documentation/#intraday

    apikey: str.
        key of API Alphavantage.

    new_database: str
        valid parameters = 'create' and 'not create'
        if there is no database, action to be taken.

    outputsize: str.
        valid parameters = 'compact' and 'full'
        compact returns only the latest 100 data points in the daily time series;
        full returns the full-length daily time series.
    '''

    def __init__(self, frecuency, apikey, outputsize='full', new_database='create', **kwargs):

        #Get outputsize
        self._outputsize = outputsize
        #Create connection to the database
        super().__init__(frecuency=frecuency, new_database=new_database)
        # Create reader from AlphaVantage
        self.__reader = Forex(apikey=apikey, **kwargs)
        self._create_dict_to_db = CreateDictsWithSameId('intraday')


    def to_database(self, from_symbol, to_symbol):

        '''
        This function save in DataBase the data of the specified pair (from_symbol, to_symbol),
        when an API error is obtained, the error returns,
        if no error is obtained, nothing returns (None)
        '''

        #Get response from reader Api Alphavantage
        response = self.__read_from_alphavantage(from_symbol, to_symbol)

        if isinstance(response, tuple):
            return response

        #Get data
        # list(response) get keys of response dict,
        # the seconds key contains the data,
        # this is test  in AlphaVantage.__read() by:
        #acquistion.errors_response.ErrorsResponseApiAlphavantage().
        key_data = list(response)[1]
        data = response[key_data]
        #Update collection
        #Get correct format
        list_dicts_to_update = self._create_dict_to_db(data)
        #Call to update
        self.update(list_dicts_to_update=list_dicts_to_update, 
                    from_symbol=from_symbol, to_symbol=to_symbol)
        return None

    def __read_from_alphavantage(self, from_symbol, to_symbol):

        '''
        This function gets the API response,
        returns a dictionary if the answer does not contain errors,
        and a list if there are errors.
        '''
        return self.__reader.get_intraday(from_symbol=from_symbol,
                                          to_symbol= to_symbol,
                                          interval=self._frecuency,
                                          outputsize=self._outputsize)

class UpdateIntradayAlphaVantageMany(UpdateIntradayAlphavantage):

    __save_many=SaveMany()
    
    def to_database_getting_errors(self, list_queries):
        return self.__save_many.save_and_return_errors(self.to_database, list_queries)

    def to_database_ignoring_errors(self, list_queries):
        return self.__save_many.save(self.to_database, list_queries)


