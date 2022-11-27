from abc import ABCMeta, abstractmethod

class TiingoToDB(metaclass=ABCMeta):
    
    @classmethod
    @property
    @abstractmethod
    def client(cls):
        pass

    @classmethod
    @property
    @abstractmethod
    def saver(cls):
        pass

    @classmethod
    @property
    @abstractmethod
    def distributor(cls):
        pass

    @classmethod
    @property
    @abstractmethod
    def evaluate_response(cls):
        pass

    @classmethod
    @property
    @abstractmethod
    def process_response(cls):
        pass

    def __call__(self, method, **params):
        response = getattr(self.client, method)(**params)
        self.evaluate_response(response)
        response_to_db = self.process_response(response)
        where_save = self.distributor(response_to_db)
        self.saver(response_to_db, where_save)
        