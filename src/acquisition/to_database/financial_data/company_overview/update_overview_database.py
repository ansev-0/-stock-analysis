from src.acquisition.to_database.financial_data.update_database import UpdateFinancialData

class UpdateOverview(UpdateFinancialData):
    def __init__(self, new_database='create'):
        super().__init__(database_name='overview')

    @UpdateFinancialData.update_data
    def update(self, collection, dict_to_update, **kwargs):

            collection.update_one({'_id' : dict_to_update['_id']},
                                  {'$set' : dict_to_update},
                                  upsert=True,
                                  **kwargs)