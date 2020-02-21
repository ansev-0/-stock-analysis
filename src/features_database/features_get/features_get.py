from src.features_database.features_database import FeaturesDataBase

class FeatureGet(FeaturesDataBase):

    def get_features(self, **kwards):
        self.features = self.__collection.find_one({'_id' : self.__document_id},
                                                   **kwards)
