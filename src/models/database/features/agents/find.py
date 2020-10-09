from src.models.database.features.agents.client import DataBaseFeatureModels

class FindFeaturesModel(DataBaseFeatureModels):

    def find_many(self, *args, **kwargs):
        return self.collection.find_many(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        return self.collection.find_one(*args, **kwargs)

    def find_path_random_model(self, path_random_model, *args, **kwargs):
        return self.find_one({'path_random_model' : path_random_model},
                             *args, **kwargs)

    def find_json_description(self, json_description, *args, **kwargs):
        return self.find_one({'json_description' : json_description},
                             *args, **kwargs)
