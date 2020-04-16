from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod
from src.data_preparation.pipeline.database import Priority
from collections import defaultdict

class Pipeline(metaclass=ABCMeta):

    _pipelines = defaultdict(int)
    _priorities = Priority()

    def __init_subclass__(cls):
        cls._priority = cls._priorities.get(cls.__name__)

    def __new__(cls):

        #only can create a new object if its class has a priority in databse.
        if cls._priority:
            #count all pipelines created
            cls._pipelines[cls.__name__] += 1
            return object.__new__(cls)
        return None

    @abstractmethod
    def _summary(self):
        pass

    @abstractmethod
    def data(self):
        pass

    @abstractclassmethod
    def process(cls):
        pass
    
    @abstractmethod
    def scalers(self):
        pass

    @property
    def priority(self):
        return self._priority

    @property
    def get_current_pipelines(self):
        return dict(self._pipelines)
