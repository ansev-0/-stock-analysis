from src.acquisition.acquisition.alphavantage.alphavantage import AlphaVantage 

class TechnicalIndicators(AlphaVantage):
    '''

    This class is used to get Techinal Indicators from Alphavantage API.
    Api reference: https://www.alphavantage.co/documentation/#technical-indicators.

    '''
    @AlphaVantage._get_data
    def get(self, function, symbol, interval, time_period=None, series_type=None):
        '''

        This function takes the necessary parameters
        to build and consult the URL of the technical indicators.

        Parameters
        -------------
        all parameters must be string.
        You must pass function symbol and interval because
        they are the parameters common to any query of this type.

        '''
        return function, symbol, interval, time_period, series_type
