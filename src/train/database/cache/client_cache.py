from src.database.database import DataBaseAdminTrainCache

class DataBaseTrainCache(DataBaseAdminTrainCache):
    
    def __init__(self, type_train):
        super().__init__('train_cache')
        self.collection = type_train

    def types_train(self, *args, **kwargs):
        return self._database.list_collection_names(*args, **kwargs)

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, type_train):
        self._collection = self._database[type_train]