from src.exceptions.to_database_exceptions import ToDataBaseAlphaVantageError
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.to_database.stock_data_intraday.errors.check_errors_intraday import CheckToDataBaseIntraday

class CheckErrorsFromAlphaVantage(CheckToDataBaseIntraday):
    '''
    This class is used to check errors related to ToDataBaseIntradayAlphaVantage.
    '''
    parameters = []
    __ID_DOCUMENT = 'alphavantage'
    def __init__(self):
        super().__init__(self, name = 'features api')
        self.update_supported_parameters()
        

    def check_frecuency_in_api(self, frecuency):
        if frecuency not  in self.parameters['frecuency']:

            raise ToDataBaseAlphaVantageError(
                f'Frequency not supported, frequencies supported are:'/
                '{self.frecuencies_intraday_in_api}', ValueError)

    @staticmethod
    def check_frecuency_in_key_data(key_data, frecuency):
        if frecuency not in key_data:
            raise ToDataBaseAlphaVantageError(f'Incorrect frecuency in response', AlphaVantageError)


