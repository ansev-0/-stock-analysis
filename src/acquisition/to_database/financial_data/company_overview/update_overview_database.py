from src.acquisition.to_database.financial_data.update_database import UpdateFinancialData

class UpdateOverview(UpdateFinancialData):
    def __init__(self, new_database='create'):
        super().__init__(database_name='stock_overview')