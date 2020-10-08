class FormQlearning(dict):

    _valid_fields = ('_id', 'stock_name', 'delays', 'based_on', 'json_architecture', 
                     'data_train_limits', 'data_validation_limits', 
                     'rewards', 'rewards_not_done', 
                     'train_states_actions', 'validation_states_actions', 
                     'actions', 'conf_train_parameters', 'call_train_parameters', 
                     'path')

    def __init__(self, **kwargs):

        super().__init__(**{self._check_key(key) : value 
                            for key, value in kwargs.items()})

    def __setitem__(self, key, value):
            super().__setitem__(self._check_key(key), value)

    def _check_key(self, key):
        if key not in self._valid_fields:
            raise KeyError('Invalid key')
        return key
        

