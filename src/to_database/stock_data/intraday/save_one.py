from src.to_database.stock_data.to_database import ToDataBaseStockData

class ToDataBaseStockDataIntraday(ToDataBaseStockData):

    def __init__(self, frecuency, new_database='create'):
        self._frecuency=frecuency
        super().__init__(database_name='stock_data_intraday_' + self._frecuency)
