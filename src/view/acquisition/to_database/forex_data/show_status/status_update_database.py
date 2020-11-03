from src.view.acquisition.to_database.show_status.status_update_database import  UpdateDataBaseShowStatus

class UpdateForexDataBaseShowStatus(UpdateDataBaseShowStatus):

    def notify_try_update_database(self, from_symbol, to_symbol, database):
        print(f'Updating {from_symbol}_TO_{to_symbol} database {self.database_name}...')
    
