from src.acquisition.to_database.stock_data.update_database import UpdateStockData

class UpdateDailyAdj(UpdateStockData):
    def __init__(self, new_database='create'):
        super().__init__(database_name='stock_data_daily_adjusted')
