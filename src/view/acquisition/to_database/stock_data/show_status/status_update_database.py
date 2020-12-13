from src.view.acquisition.to_database.show_status.status_update_database import  UpdateDataBaseShowStatus

class UpdateStockDataBaseShowStatus(UpdateDataBaseShowStatus):


    def notify_try_update_database(self, company, database):
        print(f'Updating {company} data base {self.database_name}...')
    

