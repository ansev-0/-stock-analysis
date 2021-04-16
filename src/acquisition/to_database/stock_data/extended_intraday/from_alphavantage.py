from src.acquisition.to_database.stock_data.intraday.update_intraday \
     import UpdateIntraday
from src.acquisition.acquisition.alphavantage import timeseries
from src.acquisition.to_database.save_many_stock_collection import UpdateManyStockData
from src.acquisition.to_database.stock_data.intraday.errors.check_errors_api.check_from_alphavantage \
    import CheckErrorsFromAlphaVantage
from src.acquisition.to_database.tools.to_database import CreateDictsWithSameId

class UpdateExtendedIntradayAlphaVantage(UpdateIntraday):

    '''
    This class is an interface to save the extended intraday data of the Alphavantage API

    Parameters
    ----------
    frecuency: str.
        frequency of the data to read,
        it must be supported by the API, consult:
        https://www.alphavantage.co/documentation/#intraday-extended

    apikey: str.
        key of API Alphavantage.

    new_database: str
        valid parameters = 'create' and 'not create'
        if there is no database for the specified frequency, action to be taken.
    '''

    def __init__(self, frecuency, apikey, new_database='create', **kwargs):

        #Create connection to the database
        super().__init__(frecuency=frecuency, new_database=new_database)
        #Check not error in frecuency
        self.__check_alphavantage = CheckErrorsFromAlphaVantage(frecuency=self._frecuency)
        self.__check_alphavantage.check_frecuency_in_api()
        # Create reader from AlphaVantage
        self.__reader = timeseries.TimeSeries(apikey=apikey, **kwargs)
        # custom dict
        self._create_dict_to_db = CreateDictsWithSameId('intraday')


    def to_database(self, company, slice):
        '''
        This function save in DataBase the data of the specified company,
        when an API error is obtained, the error returns,
        if no error is obtained, nothing returns (None)
        '''

        #Get response from reader Api Alphavantage
        response = self.__read_from_alphavantage(company=company, slice=slice)

        if isinstance(response, tuple):
            return response
        #Update collection
        #Get correct format
        list_dicts_to_update = self._create_dict_to_db(response)
        #Call to update
        self.update(list_dicts_to_update=list_dicts_to_update, company=company)

        return None

    def __read_from_alphavantage(self, company, slice):
        '''
        This function gets the API response,
        returns a dictionary if the answer does not contain errors,
        and a list if there are errors.
        '''
        return self.__reader.get_extended_intraday(symbol=company,
                                                   interval=self._frecuency,
                                                   slice=slice)

    @classmethod
    def slice_1min(cls, apikey, **kwargs):
        return cls(frecuency='1min', apikey=apikey, **kwargs)

    @classmethod
    def slice_5min(cls, apikey, **kwargs):
        return cls(frecuency='5min', apikey=apikey, **kwargs)

    @classmethod
    def slice_15min(cls, apikey, **kwargs):
        return cls(frecuency='15min', apikey=apikey, **kwargs)


    @classmethod
    def slice_30min(cls, apikey, **kwargs):
        return cls(frecuency='30min', apikey=apikey, **kwargs)

    @classmethod
    def slice_60min(cls, apikey, **kwargs):
        return cls(frecuency='60min', apikey=apikey, **kwargs)



class UpdateExtendedIntradayAlphaVantageMany(UpdateExtendedIntradayAlphaVantage, UpdateManyStockData):
    pass


#from itertools import product
#from pymongo import MongoClient      
#client = MongoClient('192.168.1.51', 27017)
#orders = client['acquisition_orders']['stock_data_intraday'].find_one({'_id' : 'alphavantage'})['orders']
#
#years = range(1, 2+1)
#months = range(1, 12 +1)
#slices = [f'year{year}month{month}' for month in months for year in years]
#'
#combs = list(product(orders, slices))
#
#obj = UpdateExtendedIntradayAlphaVantageMany.slice_1min(appkey)
#obj.to_database_getting_errors(combs[-500:])
