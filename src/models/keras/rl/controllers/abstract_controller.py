from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod

#from collections import defaultdict

class ControllerTransitions(metaclass=ABCMeta):

    @abstractmethod
    def eval(self):
        pass

    @abstractproperty
    def actions(self):
        pass