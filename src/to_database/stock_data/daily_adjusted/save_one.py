from src.to_database.stock_data.to_database import ToDataBaseStockData

class ToDataBaseStockDataDailyAdj(ToDataBaseStockData):
    def __init__(self, new_database='create'):
        super().__init__(database_name='stock_data_daily_adjusted')
