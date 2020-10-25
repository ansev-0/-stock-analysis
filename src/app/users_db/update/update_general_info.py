from src.app.users_db.database import DataBaseUsersGeneralInfo
from src.app.users_db.forms.general_info import general_info_valid_fields
from src.app.users_db.update.update import UpdateDataBaseUsers
from datetime import datetime
import numpy as np

class UpdateGeneralInfoDataBaseUsers(DataBaseUsersGeneralInfo, UpdateDataBaseUsers):

    _valid_external_fields = tuple(filter(lambda field: 'date_last_change' not in field,
                                   general_info_valid_fields)
                         )
    
    @property
    def valid_fields(self):
        return self._valid_external_fields

    def update_one(self, where, dict_update, **kwargs):
        # check there are only external fields
        self._check_invalid_fields(dict_update)
        # update with external fields and new datetime 
        return super().update_one(where, 
                                  self._update_with_date_last_change(dict_update),
                                  **kwargs)

    def update_many(self, where, dict_update, **kwargs):
        # check there are only external fields
        self._check_invalid_fields(dict_update)
        # update with external fields and new datetime 
        return super().update_many(where, 
                                   self._update_with_date_last_change(dict_update),
                                   **kwargs)

    def update_by_username(self, username, dict_update, **kwargs):
        self._update_by_field('username', username, dict_update, **kwargs)

    def update_by_email(self, email, dict_update, **kwargs):
        self._update_by_field('email',email, dict_update, **kwargs)

    def _update_by_field(self, field, val_field, dict_update, **kwargs):
        self.update_one({field : val_field}, dict_update, **kwargs)

    def _update_with_date_last_change(self, dict_update):
        date_now = datetime.now()
        return dict(dict_update, **{f'date_last_change_{key}' : date_now 
                                    for key, value in dict_update.items()})


    def _check_invalid_fields(self, dict_update):
        if not np.all(np.isin(list(dict_update), self._valid_external_fields)):
            valid_fields = ', '.join(self._valid_external_fields)
            raise KeyError(f'Invalid fields,  valid fields are {valid_fields}')