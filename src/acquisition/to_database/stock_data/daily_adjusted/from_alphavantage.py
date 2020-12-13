from src.acquisition.to_database.stock_data.daily_adjusted.update_daily_adjusted \
     import UpdateDailyAdj
from src.acquisition.acquisition.alphavantage.timeseries import TimeSeries
from src.acquisition.to_database.tools.to_database import CreateDictsWithSameId
from src.acquisition.to_database.save_many_stock_collection import UpdateManyStockData


class UpdateDailyAdjAlphaVantage(UpdateDailyAdj):
    '''
    This class is an interface to save the daily adjusted data of the Alphavantage API

    Parameters
    ----------

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
    def __init__(self, apikey, outputsize='full', new_database='create', **kwargs):

        #Get outputsize
        self._outputsize = outputsize
        #Create connection to the database
        super().__init__(new_database=new_database)
        # Create reader from AlphaVantage
        self.__reader = TimeSeries(apikey=apikey, **kwargs)
        self._create_dict_to_db = CreateDictsWithSameId('daily')


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
        self.update(list_dicts_to_update=list_dicts_to_update, company=company)

        return None


    def __read_from_alphavantage(self, company):
        '''
        This function gets the API response,
        returns a dictionary if the answer does not contain errors,
        and a list if there are errors.
        '''
        return self.__reader.get_daily_adjusted(symbol=company,
                                                outputsize=self._outputsize)

    @classmethod
    def full(cls, apikey, **kwargs):
        return cls(apikey=apikey, outputsize='full', **kwargs)

    @classmethod
    def compact(cls, apikey, **kwargs):
        return cls(apikey=apikey, outputsize='compact', **kwargs)


class UpdateDailyAdjAlphaVantageMany(UpdateDailyAdjAlphaVantage, UpdateManyStockData):
    pass
