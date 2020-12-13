from src.database.database import DataBaseAdminAcquisition
from src.view.acquisition.to_database.forex_data.show_status.status_update_database import UpdateForexDataBaseShowStatus
from src.acquisition.to_database.check_update_database import CheckErrorsUpdateDataBase

class UpdateForexData(DataBaseAdminAcquisition):

    def __init__(self, database_name, new_database='create'):
        self.check_errors = CheckErrorsUpdateDataBase()
        #check parameter new_database is correct
        self.check_errors.check_parameter_create(new_database)
        #create connection
        if new_database == 'not create':
            self.check_errors.check_database_exists(database_name)
        super().__init__(database_name)
        #Create object to notify events
        self.show_status =  UpdateForexDataBaseShowStatus(database_name)


    def update(self, list_dicts_to_update, from_symbol, to_symbol, **kwargs):
        collection = self.database[f'{from_symbol}_TO_{to_symbol}']
        self.show_status.notify_try_update_database(from_symbol=from_symbol, to_symbol=to_symbol,
                                                    database=self.database)
        for dict_to_update in list_dicts_to_update:
            collection.update_one({'_id' : dict_to_update['_id']},
                                  {'$set' : dict_to_update['data']},
                                  upsert=True,
                                  **kwargs)
        self.show_status.notify_database_updated()

