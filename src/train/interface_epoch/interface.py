from abc import ABCMeta, abstractmethod, abstractproperty

from src.train.interface_epoch.check import CheckInterfaceInputs

class Interface(metaclass=ABCMeta):
    _check_inputs = CheckInterfaceInputs()
    
    @abstractmethod
    def get(self):
        pass

    @abstractproperty
    def channels(self):
        pass

    @abstractproperty
    def source_data(self):
        pass

    @staticmethod
    def _get_channel_inputs(channel):
        return channel.__call__.__code__.co_varnames[1:]

