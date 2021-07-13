from abc import ABCMeta, abstractmethod

class ProcessResponse(metaclass=ABCMeta):

    '''
    abstractclass to process json response
    '''
    
    @abstractmethod
    def filter_fields(self):
        pass

    @abstractmethod
    def rename_fields(self):
        pass

    @abstractmethod
    def change_type_fields(self):
        pass
    
    @abstractmethod
    def mapper_fields(self):
        pass

    @abstractmethod
    def build_struct_to_db(self):
        pass

    @abstractmethod
    def __call__(self):
        pass