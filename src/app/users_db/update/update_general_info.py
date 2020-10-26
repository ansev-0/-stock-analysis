from src.app.users_db.database import DataBaseUsersGeneralInfo
from src.app.users_db.update.update import UpdateDataBaseUsers
from src.app.users_db.ops_to_db import OpsFieldsToDB
from src.app.users_db.forms.general_info import general_info_fields
from datetime import datetime
import numpy as np

class UpdateGeneralInfoDataBaseUsers(DataBaseUsersGeneralInfo, UpdateDataBaseUsers):

    _to_db_admin_fields = OpsFieldsToDB(general_info_fields)

    def update_one(self, where, dict_update, **kwargs):
        # check there are only external fields
        self._to_db_admin_fields.check_invalid_fields_in_dict_data(dict_update)
        # update with external fields and new datetime 
        return super().update_one(where, 
                                  self._to_db_admin_fields.build_with_date_last_change(dict_update),
                                  **kwargs)

    def update_many(self, where, dict_update, **kwargs):
        # check there are only external fields
        self._to_db_admin_fields.check_invalid_fields_in_dict_data(dict_update)
        # update with external fields and new datetime 
        return super().update_many(where, 
                                   self._to_db_admin_fields.build_with_date_last_change(dict_update),
                                   **kwargs)

    def update_by_username(self, username, dict_update, **kwargs):
        return self._update_by_field('username', username, dict_update, **kwargs)

    def update_by_email(self, email, dict_update, **kwargs):
        return self._update_by_field('email',email, dict_update, **kwargs)

    def _update_by_field(self, field, val_field, dict_update, **kwargs):
        return self.update_one({field : val_field}, dict_update, **kwargs)

    def user_confirmed(self, token, online=True):
        return self.update_one(where={'confirmed' : token}, 
                               dict_update={'confirmed' : True, 
                                            'online' : online})

    def user_logout(self, username):
        return self.update_by_username(username, {'online' : False})