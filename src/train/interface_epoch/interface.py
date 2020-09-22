from abc import ABCMeta, abstractmethod

from src.train.interface_epoch.check import CheckInterfaceInputs

class Interface(metaclass=ABCMeta):
    _check_inputs = CheckInterfaceInputs()
    
    @abstractmethod
    def get(self):
        pass

    