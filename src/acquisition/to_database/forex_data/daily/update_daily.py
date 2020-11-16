from src.acquisition.to_database.forex_data.update_database import UpdateForexData

class UpdateDaily(UpdateForexData):
    def __init__(self, new_database='create'):
        super().__init__(database_name='forex_data_daily')
