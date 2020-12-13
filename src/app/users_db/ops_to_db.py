from datetime import datetime
import numpy as np

class OpsFieldsToDB:

    def __init__(self, valid_fields):
        self._valid_fields = valid_fields

    @property
    def valid_fields(self):
        return self._valid_fields

    def check_invalid_fields_in_dict_data(self, dict_data):
        if not np.all(np.isin(list(dict_data), self._valid_fields)):
            valid_fields = ', '.join(self._valid_fields)
            raise KeyError(f'Invalid fields,  valid fields are {valid_fields}')

    def build_with_date_last_change(self, register_dict_data):
        date_now = datetime.now()
        return dict(register_dict_data, **{f'date_last_change_{key}' : date_now 
                                    for key, value in register_dict_data.items()})
    