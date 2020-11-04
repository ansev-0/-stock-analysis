from src.acquisition.to_database.save_from_api import SaveDataFromApi
from src.view.acquisition.to_database.forex_data.show_status.status_save_forex_data import SaveForexDataShowStatus
from src.acquisition.to_database.forex_data.errors.check_save_from_api \
    import CheckErrorsSaveForexDataFromApi
from src.acquisition.to_database.forex_data.intraday import from_alphavantage as intraday_alphavantage
from src.acquisition.to_database.forex_data.daily import from_alphavantage as daily_alphavantage


class SaveForexDataFromApi(SaveDataFromApi):

    def __init__(self, api, collection, data_collector):

        self._check_errors = CheckErrorsSaveForexDataFromApi(api=api, collection=collection)
        super().__init__(api, collection, data_collector)
        self.api = api
        self._show_status=SaveForexDataShowStatus()


    @property
    def check_errors(self):
        return self._check_errors

    @property
    def show_status(self):
        return self._show_status


    @classmethod
    def intraday_alphavantage(cls, frecuency, apikey, **kwargs):
        class_collector = cls.__get_intraday_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(frecuency=frecuency,
                                                  apikey=apikey, **kwargs),
                   collection='forex_data_intraday')
    @classmethod
    def daily_alphavantage(cls, apikey, **kwargs):
        class_collector = cls.__get_daily_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(apikey=apikey, **kwargs),
                   collection='forex_data_daily')

    @classmethod
    def __get_intraday_collector(cls, api):
        return {'alphavantage' : intraday_alphavantage.UpdateIntradayAlphaVantageMany}[api]

    @classmethod
    def __get_daily_collector(cls, api):
        return {'alphavantage' : daily_alphavantage.UpdateDailyAlphaVantageMany}[api]

