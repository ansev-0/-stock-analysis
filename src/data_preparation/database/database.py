from src.database.database import DataBase
from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod

class DataPreparationDataBase(metaclass=ABCMeta):

    def __init__(self):
        self._database = DataBase()
        self._database.connect('data_preparation')
        

    @abstractproperty
    def _collection(self):
        pass

    @property
    def collection_name(self):
        return self._collection