class ToDataBaseShowStatus:

    def __init__(self, database_name):
        self.database_name = database_name
    
    def notify_try_update_database(self, company, database):
        print(f'Updating {company} data base {self.database_name}...')
    
    def notify_database_updated(self):
        print(f'Data Base {self.database_name} updated successfully\n')
