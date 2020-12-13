from src.database.features_database.features_database import FeaturesDataBase

class FeatureRecords(FeaturesDataBase):


    def push_features(self, data, **kwargs):
        self._collection.update_one({'_id' : self._document_id},
                                    {'$set' : data},
                                    upsert=True,
                                    **kwargs)
    def delete_features(self, **kwargs):
        self._collection.delete_one({'_id' : self._document_id}, **kwargs)
