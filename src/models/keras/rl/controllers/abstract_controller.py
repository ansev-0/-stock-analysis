from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod

#from collections import defaultdict

class ControllerTransitions(metaclass=ABCMeta):

    @abstractmethod
    def eval_with_rewards(self):
        pass
    def eval_without_rewards(self):
        pass
    @abstractproperty
    def actions(self):
        pass