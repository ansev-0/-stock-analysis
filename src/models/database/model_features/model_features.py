from src.database.database import DataBaseAdminModelFeatures

class DataBaseModelFeatures(DataBaseAdminModelFeatures):
    def __init__(self, collection):
        super().__init__('model_features')
        self.collection = collection
        

    def collection_names(self, *args, **kwargs):
        return self._database.list_collection_names(*args, **kwargs)

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, collection):
        self._collection = self._database[collection]