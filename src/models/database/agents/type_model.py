from src.models.database.model_features.agents.agents import DataBaseAgentsModelFeatures
from abc import ABCMeta, abstractproperty

class AgentType(metaclass=ABCMeta):

    '''
    In order to manage type_model.
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


