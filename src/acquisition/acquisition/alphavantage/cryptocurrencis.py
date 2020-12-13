from src.acquisition.acquisition.alphavantage.alphavantage import AlphaVantage 

class Cryptocurrencis(AlphaVantage):
    '''

    This class is used to get Cryptocurrencis data from Alphavantage API.
    Api reference: https://www.alphavantage.co/documentation/#digital-currency.

    '''

    @AlphaVantage._get_data
    def get_exchange_rate(self, from_currency, to_currency):
        FUNCTION = 'CURRENCY_EXCHANGE_RATE'
        return from_currency, to_currency, FUNCTION

    @AlphaVantage._get_data
    def get_digital_currency_daily(self, symbol, market):
        FUNCTION = 'DIGITAL_CURRENCY_DAILY'
        return symbol, market, FUNCTION

    @AlphaVantage._get_data
    def get_digital_currency_weekly(self, symbol, market):
        FUNCTION = 'DIGITAL_CURRENCY_WEEKLY'
        return symbol, market, FUNCTION

    @AlphaVantage._get_data
    def get_digital_currency_monthly(self, symbol, market):
        FUNCTION = 'DIGITAL_CURRENCY_MONTHLY'
        return symbol, market, FUNCTION

