from src.acquisition.to_database.stock_data.update_database import UpdateStockData

class UpdateIntraday(UpdateStockData):

    def __init__(self, frecuency, new_database='create'):
        self._frecuency=frecuency
        super().__init__(database_name=f'stock_data_intraday_{self._frecuency}')
