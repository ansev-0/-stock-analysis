from src.features_database.features_database import FeaturesDataBase

class FeatureRecords(FeaturesDataBase):

    def push_features(self, data, **kwards):
        self._collection.update_one({'_id' : self._document_id},
                                    {'$set' : data},
                                    upsert=True,
                                    **kwards)
    def delete_features(self, **kwards):
        self._collection.delete_one({'_id' : self._document_id}, **kwards)
