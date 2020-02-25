from src.to_database.stock_data_intraday import todatabase_intraday
from src.to_database.stock_data_intraday import from_alphavantage
from src.to_database.stock_data_intraday.errors.check_errors \
    import CheckErrorsSaveStockDataIntraday


class SaveStockData:

    def __init__(self, api, apikey, class_save, frecuency, **kwards):
        self.__check_errors = CheckErrorsSaveStockDataIntraday(api=api)
        self.to_database = class_save(frecuency=frecuency, apikey=apikey, **kwards)

    @classmethod
    def from_alphavantage(cls, frecuency, apikey, **kwards):
        return cls(api='alphavantage',
                   apikey=apikey,
                   frecuency=frecuency,
                   class_save=from_alphavantage.ToDataBaseIntradayAlphaVantageMany,
                   **kwards)