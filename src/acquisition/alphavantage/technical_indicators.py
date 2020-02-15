from src.acquisition.alphavantage.alphavantage import AlphaVantage

class TechnicalIndicators(AlphaVantage):

    @AlphaVantage._get_data
    def get(self, function, symbol, interval, time_period=None, series_type = None):
        return function, symbol, interval, time_period, series_type