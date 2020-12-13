from abc import ABCMeta, abstractproperty

class UpdateDataBaseUsers(metaclass=ABCMeta):

    @abstractproperty
    def collection(self):
        pass

    def update_one(self, where, dict_update, **kwargs):
        return self.collection.update_one(where, self._build_with_set(dict_update), **kwargs)

    def update_many(self, where, dict_update, **kwargs):
        return self.collection.update_many(where, self._build_with_set(dict_update), **kwargs)

    @staticmethod
    def _build_with_set(dict_update):
        return {'$set' : dict_update}

