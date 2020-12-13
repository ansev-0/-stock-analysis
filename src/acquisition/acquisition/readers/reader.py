from abc import ABCMeta, abstractproperty, abstractmethod
from src.view.acquisition.reader import ReaderShowStatus

class Reader(metaclass=ABCMeta):

    _reader_shiw_status = ReaderShowStatus()
    
    @abstractproperty
    def base_url(self):
        pass

    @abstractmethod
    def __call__(self):
        pass




    