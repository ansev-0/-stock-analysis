from src.database.database import DataBaseAdminDataDataPreparation
from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod

class DataPreparationDataBase(metaclass=ABCMeta):

    def __init__(self):
        self._database = DataBaseAdminDataDataPreparation('data_preparation')

    @abstractproperty
    def _collection(self):
        pass

    @property
    def collection_name(self):
        return self._collection