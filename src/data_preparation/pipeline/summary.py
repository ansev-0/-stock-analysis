from functools import wraps
from abc import ABCMeta, abstractmethod

class Summary(metaclass = ABCMeta):

    def __init__(self):
        self._registry = None
        self.reset_str_summary()

    @abstractmethod
    def enter_params(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @property
    def registry(self):
        return self._registry

    @property
    def show(self):
        print(self._str_summary)


    def reset_str_summary(self):
        self._str_summary = None

    @classmethod
    def register(cls, function):

        @wraps(function)
        def register_dict(self, priority, *args, **kwargs):
            #default summary 
            default_fields_params_all = {'priority' : priority}
            #type pipeline summary
            default_params, additional_fields_params = function(self, *args, **kwargs)
            #get default fields
            default_fields = tuple(filter(lambda field: field != 'self', function.__code__.co_varnames))
            self._registry = dict(default_fields_params_all,
                                  **dict(zip(default_fields, default_params)), 
                                  **additional_fields_params)
        return register_dict


