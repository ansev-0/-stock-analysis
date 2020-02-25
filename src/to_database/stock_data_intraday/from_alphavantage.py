from collections import defaultdict
import pandas as pd
from src.to_database.stock_data_intraday.todatabase_intraday import ToDataBaseIntraday
from src.acquisition.alphavantage import timeseries
from src.to_database.stock_data_intraday.errors.check_errors_api.check_from_alphavantage \
    import CheckErrorsFromAlphaVantage

class ToDataBaseIntradayAlphaVantage(ToDataBaseIntraday):
    '''
    This class is an interface to save the intraday data of the Alphavantage API

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
        if there is no database for the specified frequency, action to be taken.

    outputsize: str.
        valid parameters = 'compact' and 'full'
        compact returns only the latest 100 data points in the intraday time series;
        full returns the full-length intraday time series.
    '''
    def __init__(self, frecuency, apikey, outputsize='full', new_database='create', **kwards):

        #Get outputsize
        self._outputsize = outputsize

        #Create connection to the database
        super().__init__(frecuency=frecuency, new_database=new_database)

        #Check not error in frecuency
        self.__check_alphavantage = CheckErrorsFromAlphaVantage(frecuency=self._frecuency)
        self.__check_alphavantage.check_frecuency_in_api()

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
            self.report_incident(api='alphavantage', tuple_error=response)
            return response

        #Get data
        # list(response) get keys of response dict,
        # the seconds key contains the data,
        # this is test  in AlphaVantage.__read() by:
        #acquistion.errors_response.ErrorsResponseApiAlphavantage().
        key_data = list(response)[1]
        data = response[key_data]
        #check frecuency in key
        self.__check_alphavantage.check_frecuency_in_key_data(key_data)
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
            cumulative_dict[date[:10]].update({date : {name[3:] : value
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
        return self.__reader.get_intraday(symbol=company,
                                          interval=self._frecuency,
                                          outputsize=self._outputsize)

    @classmethod
    def full_1min(cls, apikey, **kwards):
        return cls(frecuency='1min', apikey=apikey, outputsize='full', **kwards)

    @classmethod
    def compact_1min(cls, apikey, **kwards):
        return cls(frecuency='1min', apikey=apikey, outputsize='compact', **kwards)

    @classmethod
    def full_5min(cls, apikey, **kwards):
        return cls(frecuency='5min', apikey=apikey, outputsize='full', **kwards)

    @classmethod
    def compact_5min(cls, apikey, **kwards):
        return cls(frecuency='5min', apikey=apikey, outputsize='compact', **kwards)

    @classmethod
    def full_15min(cls, apikey, **kwards):
        return cls(frecuency='15min', apikey=apikey, outputsize='full', **kwards)

    @classmethod
    def compact_15min(cls, apikey, **kwards):
        return cls(frecuency='15min', apikey=apikey, outputsize='compact', **kwards)


    @classmethod
    def full_30min(cls, apikey, **kwards):
        return cls(frecuency='30min', apikey=apikey, outputsize='full', **kwards)

    @classmethod
    def compact_30min(cls, apikey, **kwards):
        return cls(frecuency='30min', apikey=apikey, outputsize='compact', **kwards)


    @classmethod
    def full_60min(cls, apikey, **kwards):
        return cls(frecuency='60min', apikey=apikey, outputsize='full', **kwards)

    @classmethod
    def compact_60min(cls, apikey, **kwards):
        return cls(frecuency='60min', apikey=apikey, outputsize='compact', **kwards)
