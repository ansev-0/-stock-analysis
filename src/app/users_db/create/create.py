from abc import ABCMeta, abstractproperty

class CreateDataBaseUsers(metaclass=ABCMeta):

    @abstractproperty
    def collection(self):
        pass

    def insert_one(self, dict_data, **kwargs):
        return self.collection.insert_one(dict_data, **kwargs)

    def insert_many(self, dict_data, **kwargs):
        return self.collection.insert_many(dict_data, **kwargs)

