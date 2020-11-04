from abc import ABCMeta, abstractproperty, abstractmethod

class Commision:
    
    @abstractproperty
    def fixed(self):
        pass

    @abstractproperty
    def variables(self):
        pass

    @property
    @classmethod
    @abstractmethod
    def measurement_units(self):
        pass
    