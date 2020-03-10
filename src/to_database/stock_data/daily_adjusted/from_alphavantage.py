from collections import defaultdict
import pandas as pd
from src.to_database.stock_data.daily_adjusted.save_one import ToDataBaseStockDataDailyAdj
from src.acquisition.alphavantage import timeseries
from src.to_database.stock_data.save_many import SaveMany


class ToDataBaseDailyAdjAlphaVantage(ToDataBaseStockDataDailyAdj):
    '''
    This class is an interface to save the daily adjusted data of the Alphavantage API

    Parameters
    ----------
    frecuency: str.
        frequency of the data to read,
        it must be supported by the API, consult:
        https://www.alphavantage.co/documentation/#dailyadj

    apikey: str.
        key of API Alphavantage.

    new_database: str
        valid parameters = 'create' and 'not create'
        if there is no database for the specified frequency, action to be taken.

    outputsize: str.
        valid parameters = 'compact' and 'full'
        compact returns only the latest 100 data points in the intraday time series;
        full returns the full-length intraday time series.
    '''
    def __init__(self, apikey, outputsize='full', new_database='create', **kwards):

        #Get outputsize
        self._outputsize = outputsize

        #Create connection to the database
        super().__init__(new_database=new_database)


        # Create reader from AlphaVantage
        self.__reader = timeseries.TimeSeries(apikey=apikey, **kwards)

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
        list_dicts_to_update = self.__create_dicts_with_same_id(data)
        #Call to update
        self.update_stock_data(list_dicts_to_update=list_dicts_to_update, company=company)

        return None

    @staticmethod
    def __create_dicts_with_same_id(data):
        '''
        This function adapts the format of the json received from the Alphavantage API
        to the format necessary to update the database using :

        update_stock_data
        '''

        cumulative_dict = defaultdict(dict)
        for date, values in data.items():
            cumulative_dict[date[:7]].update({date : {name[3:] : value
                                                       for name, value in values.items()}})

        return list(map(lambda items: {'_id' : pd.to_datetime(items[0]),
                                       'data' : items[1]},
                        cumulative_dict.items())
                   )


    def __read_from_alphavantage(self, company):
        '''
        This function gets the API response,
        returns a dictionary if the answer does not contain errors,
        and a list if there are errors.
        '''
        return self.__reader.get_daily_adjusted(symbol=company,
                                                outputsize=self._outputsize)

    @classmethod
    def full(cls, apikey, **kwards):
        return cls(apikey=apikey, outputsize='full', **kwards)

    @classmethod
    def compact(cls, apikey, **kwards):
        return cls(apikey=apikey, outputsize='compact', **kwards)


class ToDataBaseDailyAdjAlphaVantageMany(ToDataBaseDailyAdjAlphaVantage):

    __save_many=SaveMany()
    
    def to_database_getting_errors(self, list_company):
        return self.__save_many.save_and_return_errors(self.to_database, list_company)

    def to_database_ignoring_errors(self, list_company):
        return self.__save_many.save(self.to_database, list_company)

