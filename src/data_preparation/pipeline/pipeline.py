from abc import ABCMeta, abstractmethod, abstractproperty
from collections import defaultdict
class Pipeline(metaclass=ABCMeta):

    _pipelines = defaultdict(int)

    def __new__(cls):
        cls._pipelines[cls.__name__] += 1 
        return object.__new__(cls)

    @abstractmethod
    def summary(self):
        pass

    @abstractproperty
    def _priority(self):
        pass

    @property
    def priority(self):
        return self._priority

    @property
    def get_current_pipelines(self):
        return self._pipelines


