from src.acquisition.to_database.save_from_api import SaveDataFromApi
from src.view.acquisition.to_database.stock_data.show_status.status_save_stock_data import SaveStockDataShowStatus
from src.acquisition.to_database.stock_data.errors.check_save_from_api \
    import CheckErrorsSaveStockDataFromApi
from src.acquisition.to_database.stock_data.intraday import from_alphavantage as intraday_alphavantage
from src.acquisition.to_database.stock_data.extended_intraday import from_alphavantage as extended_intraday_alphavantage
from src.acquisition.to_database.stock_data.daily_adjusted import from_alphavantage as dailyadj_alphavantage



class SaveStockDataFromApi(SaveDataFromApi):

    def __init__(self, api, collection, data_collector):

        self._check_errors = CheckErrorsSaveStockDataFromApi(api=api, collection=collection)
        super().__init__(api, collection, data_collector)
        self.api = api
        self._show_status=SaveStockDataShowStatus()

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
                   collection='stock_data_intraday')

    @classmethod
    def extended_intraday_alphavantage(cls, frecuency, apikey, **kwargs):

        return cls(api='alphavantage',
                   data_collector=extended_intraday_alphavantage.UpdateExtendedIntradayAlphaVantageMany(frecuency=frecuency,
                                                                                                        apikey=apikey, **kwargs),
                   collection='stock_data_intraday')

    @classmethod
    def dailyadj_alphavantage(cls, apikey, **kwargs):
        class_collector = cls.__get_dailyadj_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(apikey=apikey, **kwargs),
                   collection='stock_data_dailyadj')

    @classmethod
    def __get_intraday_collector(cls, api):
        return {'alphavantage' : intraday_alphavantage.UpdateIntradayAlphaVantageMany}[api]

    @classmethod
    def __get_dailyadj_collector(cls, api):
        return {'alphavantage' : dailyadj_alphavantage.UpdateDailyAdjAlphaVantageMany}[api]
