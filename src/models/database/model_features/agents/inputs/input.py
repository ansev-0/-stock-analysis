class InputModel(dict):

    _valid_keys = ('features', 'delays', 'frecuency', 'scaler')

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
          self[key] = value

    def __setitem__(self, key, value):

        if not key in self._valid_keys:
            raise KeyError(f'Valid keys : {self._valid_keys}')
        super().__setitem__(key, value)

