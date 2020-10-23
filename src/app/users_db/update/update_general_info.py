from src.app.users_db.database import DataBaseUsersGeneralInfo
from src.app.users_db.forms.general_info import general_info_valid_fields
from src.app.users_db.update.update import UpdateDataBaseUsers
import numpy as np

class UpdateGeneralInfoDataBaseUsers(DataBaseUsersGeneralInfo, UpdateDataBaseUsers):

    def update_one(self, where, dict_update, **kwargs):
        self._check_invalid_fields(dict_update)
        return super().update_one(where, dict_update, **kwargs)

    def update_many(self, where, dict_update, **kwargs):
        self._check_invalid_fields(dict_update)
        return super().update_many(where, dict_update, **kwargs)

    def update_by_username(self, username, dict_update, **kwargs):
        self._update_by_field('username', username, dict_update, **kwargs)

    def update_by_email(self, email, dict_update, **kwargs):
        self._update_by_field('email',email, dict_update, **kwargs)

    def _update_by_field(self, field, val_field, dict_update, **kwargs):
        self.update_one({field : val_field}, dict_update, **kwargs)

    @staticmethod
    def _check_invalid_fields(dict_update):
        if not np.all(np.isin(list(dict_update), general_info_valid_fields)):
            valid_fields = ', '.join(general_info_valid_fields)
            raise KeyError(f'Invalid fields,  valid fields are {valid_fields}')