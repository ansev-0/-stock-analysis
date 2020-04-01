from src.exceptions.to_database_exceptions import ToDataBaseAlphaVantageError
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.database.features_database.features_get import FeatureGet

class CheckErrorsFromAlphaVantage:
    '''
    This class is used to check errors related to ToDataBaseIntradayAlphaVantage.
    '''

    def __init__(self, frecuency):
        self.features_get = FeatureGet.api_alphavantage(collection='stock_data_intraday')
        self.features_get.get_features()
        self.__frecuency = frecuency

    def check_frecuency_in_api(self):
        if self.__frecuency not  in self.features_get.features['frecuency']:

            raise ToDataBaseAlphaVantageError(
                f'Frequency not supported, frequencies supported are:'/
                '{self.frecuencies_intraday_in_api}', ValueError)


    def check_frecuency_in_key_data(self, key_data):
        if self.__frecuency not in key_data:
            raise ToDataBaseAlphaVantageError(f'Incorrect frecuency in response', AlphaVantageError)


