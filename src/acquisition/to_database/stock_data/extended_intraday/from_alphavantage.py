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

    : str.
        key of API Alphavantage.

    new_database: str
        valid parameters = 'create' and 'not create'
        if there is no database for the specified frequency, action to be taken.
    '''

    def __init__(self, frecuency, new_database='create', **kwargs):

        #Create connection to the database
        super().__init__(frecuency=frecuency, new_database=new_database)
        #Check not error in frecuency
        self.__check_alphavantage = CheckErrorsFromAlphaVantage(frecuency=self._frecuency)
        self.__check_alphavantage.check_frecuency_in_api()
        # Create reader from AlphaVantage
        self.__reader = timeseries.TimeSeries(**kwargs)
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
    def slice_1min(cls, **kwargs):
        return cls(frecuency='1min', **kwargs)

    @classmethod
    def slice_5min(cls, **kwargs):
        return cls(frecuency='5min', **kwargs)

    @classmethod
    def slice_15min(cls, **kwargs):
        return cls(frecuency='15min', **kwargs)

    @classmethod
    def slice_30min(cls, **kwargs):
        return cls(frecuency='30min', **kwargs)

    @classmethod
    def slice_60min(cls, **kwargs):
        return cls(frecuency='60min', **kwargs)



class UpdateExtendedIntradayAlphaVantageMany(UpdateExtendedIntradayAlphaVantage, UpdateManyStockData):
    pass


#if __name__ == '__main__':
#    years = range(1, 3)
#    months = range(1, 13)
#    l = [f'year{year}month{month}' for year in years for month in months]
#    from src.acquisition.acquisition_orders.orders import AcquisitionOrders
#    orders = AcquisitionOrders('stock_data_intraday').get_acquisition_api_orders('alphavantage')
#    queries = [(order, rang) for order in orders for rang in l]
#    UpdateExtendedIntradayAlphaVantageMany('1min').to_database_getting_errors(queries[:100])