from src.acquisition.to_database.financial_data.update_database import UpdateFinancialData

class UpdateFinancialFeatureData(UpdateFinancialData):

    @UpdateFinancialData.update_data
    def update(self, collection, list_dicts_to_update, **kwargs):
        for dict_to_update in list_dicts_to_update:
            collection.update_one({'_id' : dict_to_update['_id']},
                                  {'$set' : dict_to_update},
                                  upsert=True,
                                  **kwargs)