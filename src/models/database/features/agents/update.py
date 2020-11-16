from src.models.database.features.agents.client import DataBaseFeatureModels


class UpdateFeaturesModel(DataBaseFeatureModels):
    
    def update_one(self, where, dict_to_update):
        return self.collection.update_one(where, {'$set' : dict_to_update})

    def update_many(self, where, dict_to_update):
        return self.collection.update_many(where, {'$set' : dict_to_update})

    def update_on_path_random_model(self, dict_to_update, path_random_model):
        return self.update_one({'path_random_model' : path_random_model}, dict_to_update)

    def update_on_json_description(self, json_description, dict_to_update):
        return self.update_one({'json_description' : json_description}, dict_to_update)
