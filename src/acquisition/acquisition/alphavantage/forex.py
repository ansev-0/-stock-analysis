from src.acquisition.acquisition.alphavantage.alphavantage import AlphaVantage 

class Forex(AlphaVantage):
    '''

    This class is used to get Forex data from Alphavantage API.
    Api reference: https://www.alphavantage.co/documentation/#fx.

    '''

    @AlphaVantage._get_data
    def get_exchange_rate(self, from_currency, to_currency):
        DATATYPE = 'json'
        FUNCTION = 'CURRENCY_EXCHANGE_RATE'
        return from_currency, to_currency, DATATYPE, FUNCTION

    @AlphaVantage._get_data
    def get_intraday(self, from_symbol, to_symbol, interval, outputsize='compact'):
        DATATYPE = 'json'
        FUNCTION = 'FX_INTRADAY'
        return from_symbol, to_symbol, interval, outputsize, DATATYPE, FUNCTION

    @AlphaVantage._get_data
    def get_daily(self, from_symbol, to_symbol, outputsize='compact'):
        DATATYPE = 'json'
        FUNCTION = 'FX_DAILY'
        return from_symbol, to_symbol, outputsize, DATATYPE, FUNCTION

    @AlphaVantage._get_data
    def get_weekly(self, from_symbol, to_symbol):
        DATATYPE = 'json'
        FUNCTION = 'FX_WEEKLY'
        return from_symbol, to_symbol, DATATYPE, FUNCTION

    @AlphaVantage._get_data
    def digital_currency_monthly(self, from_symbol, to_symbol):
        DATATYPE = 'json'
        FUNCTION = 'FX_MONTHLY'
        return from_symbol, to_symbol, DATATYPE, FUNCTION
