from src.features_database.features_database import FeaturesDataBase

class FeatureGet(FeaturesDataBase):

    def get_features(self, **kwards):
        self.features = self._collection.find_one({'_id' : self._document_id},
                                                  **kwards)
