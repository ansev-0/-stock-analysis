from src.acquisition.alphavantage.alphavantage import AlphaVantage 

class TimeSeries(AlphaVantage):
    
    @AlphaVantage._get_data
    def get_intraday(self, symbol, interval, outputsize = 'compact'):
        FUNCTION = 'TIME_SERIES_INTRADAY'
        return symbol, interval, outputsize, FUNCTION

    @AlphaVantage._get_data
    def get_daily(self, symbol, outputsize='compact'):
        FUNCTION = 'TIME_SERIES_DAILY'
        return symbol, outputsize, FUNCTION

    @AlphaVantage._get_data
    def get_daily_adjusted(self, symbol, outputsize='compact'):
        FUNCTION = 'TIME_SERIES_DAILY_ADJUSTED'
        return symbol, outputsize, FUNCTION

    @AlphaVantage._get_data
    def get_weekly(self, symbol):
        FUNCTION = 'TIME_SERIES_WEEKLY'
        return symbol, FUNCTION

    @AlphaVantage._get_data
    def get_weekly_adjusted(self, symbol):
        FUNCTION = 'TIME_SERIES_WEEKLY_ADJUSTED'
        return symbol, FUNCTION


    @AlphaVantage._get_data
    def get_monthly(self, symbol):
        FUNCTION = 'TIME_SERIES_MONTHLY'
        return symbol, FUNCTION

    @AlphaVantage._get_data
    def get_monthly_adjusted(self, symbol):
        FUNCTION = 'TIME_SERIES_MONTHLY_ADJUSTED'
        return symbol, FUNCTION


    @AlphaVantage._get_data
    def get_quote_endpoint(self, symbol):
        FUNCTION = 'GLOBAL_QUOTE'
        return symbol, FUNCTION







    
    