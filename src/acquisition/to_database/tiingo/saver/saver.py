from src.database.database import DataBaseAdminTiingo
from abc import ABCMeta, abstractmethod

class SaverTiingo(DataBaseAdminTiingo, metaclass=ABCMeta):

    @classmethod
    @property
    @abstractmethod
    def tiingo_db(cls):
        pass

    def __init__(self, collection=None):
        super().__init__(database_name=self.tiingo_db)
        if collection is not None:
            self.collection = collection

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, collection):
        self._collection = self._database[collection.upper()]

    @DataBaseAdminTiingo.try_and_wakeup
    def update_one(self, *args, **kwargs):
        return self.collection.update_one(*args, **kwargs)

    @DataBaseAdminTiingo.try_and_wakeup
    def update_many(self, *args, **kwargs):
        return self.collection.update_many(*args, **kwargs)

    