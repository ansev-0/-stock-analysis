from src.acquisition.alphavantage.alphavantage import AlphaVantage 

class Cryptocurrencis(AlphaVantage):

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

Cryptocurrencis(apikey = 'O39L8VIVYYJYUN3P').get_exchange_rate(from_currency='USD', to_currency='BTC')