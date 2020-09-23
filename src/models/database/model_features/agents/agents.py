from src.models.database.model_features.model_features import DataBaseModelFeatures

class DataBaseAgentsModelFeatures(DataBaseModelFeatures):

    def __init__(self):
        super().__init__('agents')

    def get_types(self):
        return set(type_model_dict['type'] for type_model_dict in 
                   self.collection.find({}, projection={'type' : 1, '_id' : 0}))