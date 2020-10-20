from abc import ABCMeta, abstractmethod
from flask import request

class BeforeRequestTask(metaclass=ABCMeta):

    def __init__(self, endpoints_task):
        self._endpoints_task = endpoints_task
    
    @property
    def endpoints_task(self):
        return self._endpoints_task

    @property
    def endpoint_in_endpoints_task(self):
        return request.endpoint in self._endpoints_task


    @abstractmethod
    def __call__(self):
        pass


