from src.database.features_database.features_database import FeaturesDataBase

class FeatureGet(FeaturesDataBase):

    def get_features(self, **kwargs):
        self.features = self._collection.find_one({'_id' : self._document_id},
                                                  **kwargs)
