class FormQlearning(dict):

    _valid_fields = ('_id', 'stock_name', 'broker', 'delays', 'based_on', 
                     'data_train_limits', 'data_validation_limits', 
                     'rewards', 'rewards_not_done', 
                     'train_states_actions', 'validation_states_actions', 
                     'actions',
                     'conf_build_agent', 'conf_call_agent', 
                     'path', 'cache_id_train', 'cache_id_validation',
                     'cache_id_commision_train', 'cache_id_commision_validation',
                     'cache_id_financial_train', 'cache_id_financial_validation')
                     
    def __init__(self, **kwargs):

        super().__init__(**{self._check_key(key) : value 
                            for key, value in kwargs.items()})

    def __setitem__(self, key, value):
            super().__setitem__(self._check_key(key), value)

    def _check_key(self, key):
        if key not in self._valid_fields:
            raise KeyError('Invalid key')
        return key
        

