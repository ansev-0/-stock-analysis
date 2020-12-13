from src.models.database.features.agents.client import DataBaseFeatureModels
from src.models.database.features.agents.form import FormFeatures

class CreateFeaturesModel(DataBaseFeatureModels):

    def from_dict(self, dict_features):
        form = FormFeatures(**dict_features)
        return self._insert(form.copy())

    def from_keys(self, json_description, path_random_model):
        form = FormFeatures(
            **dict(
                zip(
                    FormFeatures.valid_fields,
                    (json_description, path_random_model)
                   )
            )
        )
        return self._insert(form.copy())

    def from_keras_model(self, model, path_random_model):
        return self.from_keys(model.to_json(), path_random_model)

    def _insert(self, form):
        return self.collection.insert_one(form)


