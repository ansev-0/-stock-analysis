from abc import ABCMeta, abstractproperty

class FindDataBaseUsers(metaclass=ABCMeta):

    @abstractproperty
    def collection(self):
        pass

    def find_one(self, where, **kwargs):
        return self.collection.find_one(where, **kwargs)

    def find(self, where, **kwargs):
        return self.collection.find(where, **kwargs)
