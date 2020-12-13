from src.database.database import DataBaseAdminAcquisition
from src.view.acquisition.to_database.stock_data.show_status.status_update_database import UpdateStockDataBaseShowStatus
from src.acquisition.to_database.check_update_database import CheckErrorsUpdateDataBase
from functools import wraps

class UpdateFinancialData(DataBaseAdminAcquisition):
    
    def __init__(self, database_name, new_database='create'):
        self.check_errors = CheckErrorsUpdateDataBase()
        #check parameter new_database is correct
        self.check_errors.check_parameter_create(new_database)
        #create connection
        if new_database == 'not create':
            self.check_errors.check_database_exists(database_name)
        super().__init__(database_name)
        #Create object to notify events
        self.show_status = UpdateStockDataBaseShowStatus(database_name)

    @classmethod   
    def update_data(cls, func):

        @wraps(func)
        def _update_with_func(self, company, *args, **kwargs):
            collection = self.database[company]
            self.show_status.notify_try_update_database(company=company, database=self.database)
            func(self, collection, *args, **kwargs)
            self.show_status.notify_database_updated()

        return _update_with_func