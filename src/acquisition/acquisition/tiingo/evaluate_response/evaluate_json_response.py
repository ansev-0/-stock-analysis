from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod

class EvaluateJsonResponse:

    @classmethod
    @property
    @abstractmethod
    def field_type_dict_response(cls):
        pass

    def __call__(self, response):
        if isinstance(dict, response):
            self._check(response)
        elif isinstance(response, list):
            map(lambda resp: self._check(resp), response)
        else:
            raise TypeError('Invalid formart response')

    def _check(self, dict_response):
        for field, _type in self.field_type_dict_response.items():
            if (not field in dict_response)\
            or not isinstance(dict_response[field], _type):
                raise ValueError('Invalid fields or types')

