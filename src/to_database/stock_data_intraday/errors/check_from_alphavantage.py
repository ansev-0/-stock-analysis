from src.exceptions.to_database_exceptions import ToDataBaseAlphaVantageError
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.to_database.stock_data_intraday.errors.check_errors_intraday import CheckToDataBaseIntraday

class CheckErrorsFromAlphaVantage(CheckToDataBaseIntraday):
    frecuencies_intraday_in_api = []
    __ID_DOCUMENT = 'alphavantage'
    def __init__(self):
        super().__init__()
        self.frecuencies_intraday_in_database = (
            self.__get_supported_frequencies(document_id=self.__ID_DOCUMENT)
            )

    def check_frecuency_in_api(self, frecuency):
        if not self.__frecuency_supported(frecuency=frecuency,
                                          list_frecuencies=self.frecuencies_intraday_in_api):

            raise ToDataBaseAlphaVantageError(
                f'Frequency not supported, frequencies supported are:'/
                '{self.frecuencies_intraday_in_api}', ValueError)

    @staticmethod
    def check_frecuency_in_key_data(key_data, frecuency):
        if frecuency not in key_data:
            raise ToDataBaseAlphaVantageError(f'Incorrect frecuency in response', AlphaVantageError)
