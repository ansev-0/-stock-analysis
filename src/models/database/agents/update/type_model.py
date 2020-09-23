from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.update import UpdateValidFieldsDocumentDB
from src.models.database.model_features.agents.agents import DataBaseAgentsModelFeatures

class UpdateAgentType(DataBaseOneAgent, UpdateValidFieldsDocumentDB):

    _valid_fields = 'type_model'

    def __init__(self, stock_name):
        super().__init__(stock_name=stock_name)

    @property
    def valid_fields(self):
        return self._valid_fields

    @property
    def valid_types(self):
        return DataBaseAgentsModelFeatures().get_types()

    def update_one(self, where, type_model, **kwargs):
        return self.collection.update_one(where, 
                                          self._dict_update(type_model), 
                                          **kwargs)

    def update_many(self, where, type_model, **kwargs):
        return self.collection.update_many(where, 
                                           self._dict_update(type_model),
                                           **kwargs)

    def _valid_type_model(self, type_model):
        valid_types = self.valid_types

        if not type_model in valid_types:
            raise ValueError(f'Invalid type model, you must pass one of {valid_types}')

    def _dict_update(self, type_model):
        return {self._valid_fields : type_model}
