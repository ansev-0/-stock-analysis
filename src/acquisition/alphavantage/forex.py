from src.acquisition.alphavantage.alphavantage import AlphaVantage 

class Forex(AlphaVantage):

    @AlphaVantage._get_data
    def get_exchange_rate(self, from_currency, to_currency):
        FUNCTION = 'CURRENCY_EXCHANGE_RATE'
        return from_currency, to_currency, FUNCTION

    @AlphaVantage._get_data
    def get_intraday(self, from_symbol, to_symbol, interval, outputsize = 'compact'):
        FUNCTION = 'FX_INTRADAY'
        return from_symbol, to_symbol, interval, outputsize, FUNCTION

    @AlphaVantage._get_data
    def get__daily(self, from_symbol, to_symbol, outputsize = 'compact'):
        FUNCTION = 'FX_DAILY'
        return from_symbol, to_symbol, outputsize, FUNCTION

    @AlphaVantage._get_data
    def get_weekly(self, from_symbol, to_symbol):
        FUNCTION = 'FX_WEEKLY'
        return from_symbol, to_symbol, FUNCTION

    @AlphaVantage._get_data
    def digital_currency_monthly(self, from_symbol, to_symbol):
        FUNCTION = 'FX_MONTHLY'
        return from_symbol, to_symbol, FUNCTION