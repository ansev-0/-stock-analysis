from src.features_database.features_database import FeaturesDataBase

class FeatureRecords(FeaturesDataBase):

    def push_features(self, data, **kwards):
        self.__collection.update_one({'_id' : self.__document_id},
                                     {'set' : data},
                                     upsert=True,
                                     **kwards)
    def delete_features(self, **kwards):
        self.__collection.delete_one({'_id' : self.__document_id}, **kwards)
