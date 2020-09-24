from src.models.database.model_features.agents.agents import DataBaseAgentsModelFeatures
from src.models.database.agents.agents import DataBaseOneAgent

class AgentIdType(DataBaseOneAgent):

    '''
    This class is used to check if the model type is allowed and to obtain the following id_type
    '''

    def __init__(self, stock_name):
        super().__init__(stock_name=stock_name)

    #public methods
    @property
    def valid_types(self):
        return DataBaseAgentsModelFeatures().get_types()

    def is_valid_type(self, type_model):
        return type_model in self.valid_types

    def get_last_id(self, type_model):
        self._check_valid_type(type_model)
        return self._try_get_id(self._find_min_id_type(type_model))

    #private methods
    def _find_min_id_type(self, type_model):
        return self.collection.find_one(filter={'type_model':type_model},
                                        sort=[("id_type", -1)], 
                                        projection={'id_type':True, '_id' : False})

    def _check_valid_type(self, type_model):
        if not self.is_valid_type(type_model):
            raise ValueError(f'''You must pass valid type_model,
                             Valid types are {self.valid_types}''')

    @staticmethod
    def _try_get_id(dict_document):
        try:
            return dict_document['id_type']
        except KeyError:
            pass
        