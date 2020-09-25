from src.models.database.model_features.agents.agents import DataBaseAgentsModelFeatures
from abc import ABCMeta, abstractproperty

class AgentIdType(metaclass=ABCMeta):
    '''
    In order to manage id_type and type_model.
    '''
    @abstractproperty
    def collection(self):
        pass

    #public methods
    @property
    def valid_types(self):
        return DataBaseAgentsModelFeatures().get_types()

    def is_valid_type(self, type_model):
        return type_model in self.valid_types

    def get_last_id(self, type_model):
        return self._try_get_id(self._find_min_id_type(type_model))

    def get_ids(self, type_model):

        return tuple(
            map(self._try_get_id,
                self.collection.find(filter={'type_model' : type_model}, 
                                     projection={'id_type' : True,
                                                 '_id' : False}
                                    )
            )
        )

    def is_valid_id_for_type_model(self, id_type, type_model):
        return id_type in self.get_ids(type_model)

    #private methods
    def _find_min_id_type(self, type_model):
        return self._try_get_id(
            self.collection.find_one(filter={'type_model' : type_model},
                                     sort=[("id_type", -1)], 
                                     projection={'id_type':True, 
                                                '_id' : False})
        )

    @staticmethod
    def _try_get_id(dict_document):
        try:
            return dict_document['id_type']
        except KeyError:
            return None
        