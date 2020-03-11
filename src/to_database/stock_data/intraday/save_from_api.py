from src.to_database.stock_data.intraday import from_alphavantage
from src.to_database.stock_data.show_status.status_save_stock_data import SaveStockDataShowStatus
from src.to_database.stock_data.save_from_api import SaveStockDataFromApi

class SaveIntradayFromApi(SaveStockDataFromApi):

    api_mapper={'alphavantage' : from_alphavantage.UpdateIntradayAlphaVantageMany}
    def __init__(self, api, apikey, frecuency, **kwards):
        
        #check method of class
        class_save=self.api_mapper[api]
        super().__init__(api=api,
                         collection='stock_data_intraday',
                         data_collector=class_save(frecuency=frecuency, apikey=apikey, **kwards)
                       )
        self.check_errors.check_methods_supported(class_save)

    @classmethod
    def from_alphavantage(cls, frecuency, apikey, **kwards):
        return cls(api='alphavantage',
                   apikey=apikey,
                   frecuency=frecuency,
                   **kwards)
