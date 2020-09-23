from abc import ABCMeta, abstractproperty

from src.tools.filter import filter_dict

class UpdateValidFieldsDocumentDB(metaclass=ABCMeta):

    @abstractproperty
    def collection(self):
        pass

    @abstractproperty
    def valid_fields(self):
        pass


    def update_many(self, where, data, **kwargs):
        return self.collection.update_many(where, 
                                           self._update_dict(data),
                                           **kwargs)

    def update_one(self, where, data, **kwargs):
        return self.collection.update_one(where, 
                                          self._update_dict(data),
                                          **kwargs)

    def _update_dict(self, data):
        return {'$set' : filter_dict(data, self.valid_fields)}


