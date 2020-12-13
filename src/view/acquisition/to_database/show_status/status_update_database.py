class UpdateDataBaseShowStatus:

    def __init__(self, database_name):
        self.database_name = database_name

    def notify_database_updated(self):
        print(f'Data Base {self.database_name} updated successfully\n')

