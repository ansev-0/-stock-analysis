from src.models.database.features.agents.client import DataBaseFeatureModels

class DeleteFeaturesModel(DataBaseFeatureModels):

    def delete_one(self, where):
        return self.collection.delete_one(where)

    def delete_many(self, where):
        return self.collection.delete_many(where)

    def delete_on_path_random_model(self, path_random_model):
        return self.delete_one({'path_random_model' : path_random_model})

    def delete_on_path_random_model(self, json_description):
        return self.delete_one({'json_description' : json_description})