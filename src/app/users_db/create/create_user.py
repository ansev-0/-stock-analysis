from src.app.users_db.create.create import CreateDataBaseUsers
from src.app.users_db.database import DataBaseUsersGeneralInfo
from src.app.users_db.forms.general_info import general_info_external_fields
from src.app.users_db.ops_to_db import OpsFieldsToDB
from datetime import datetime
import numpy as np

class CreateNewUser(DataBaseUsersGeneralInfo, CreateDataBaseUsers):

    _to_db_admin_fields = OpsFieldsToDB(general_info_external_fields)


    def __call__(self, register_dict_data, token):
        # check there are only valids external fields
        self._to_db_admin_fields.check_invalid_fields_in_dict_data(register_dict_data)
        # insert confirmed False
        register_dict_data = self._add_token_confirm(register_dict_data, token)
        # create with external fields and datetime 
        return super().insert_one(
            self._to_db_admin_fields.build_with_date_last_change(register_dict_data)
            )

    @staticmethod
    def _add_token_confirm(register_dict_data, token):
        return dict(register_dict_data, **{'confirmed' : token})

