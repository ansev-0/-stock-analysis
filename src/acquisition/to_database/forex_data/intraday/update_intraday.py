from src.acquisition.to_database.forex_data.update_database import UpdateForexData

class UpdateIntraday(UpdateForexData):
    def __init__(self, frecuency, new_database='create'):
        self._frecuency=frecuency
        super().__init__(database_name=f'forex_data_intraday_{self._frecuency}')
