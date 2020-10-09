class FormFeatures(dict):

    valid_fields = ('json_description', 'path_random_model')

    def __init__(self, **kwargs):
        super().__init__(**{self._check_valid_fields(key) : value 
                            for key, value in kwargs.items()})

    def __setitem__(self, key, value):
        return super().__setitem__(self._check_valid_fileds(key), value)

    def _check_valid_fields(self, key):
        if key not in self.valid_fields:
            raise KeyError('You must pass a valid field')
        return key


