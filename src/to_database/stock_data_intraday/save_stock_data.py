from src.to_database.stock_data_intraday import todatabase_intraday
from src.to_database.stock_data_intraday import from_alphavantage
from src.to_database.stock_data_intraday.errors.check_errors \
    import CheckErrorsSaveStockDataIntraday
from src.database.database import DataBase


class SaveStockData(DataBase):

    def __init__(self, api, apikey, class_save, frecuency, **kwards):
        self.api=api
        self.__check_errors = CheckErrorsSaveStockDataIntraday(api=api)
        #check api supported
        self.__check_errors.check_api_supported()
        #check method of class
        self.__check_errors.check_methods_supported(class_save)
        self.to_database = class_save(frecuency=frecuency, apikey=apikey, **kwards)
        #create connect with collection of orders
        super().__init__(name_database='acquisition orders')

        
    @classmethod
    def from_alphavantage(cls, frecuency, apikey, **kwards):
        return cls(api='alphavantage',
                   apikey=apikey,
                   frecuency=frecuency,
                   class_save=from_alphavantage.ToDataBaseIntradayAlphaVantageMany,
                   **kwards)
   


    def __get_orders(self):
        return self.database['stock_data_intraday'].find_one({'_id' : self.api},
                                                             projection='orders')['orders']