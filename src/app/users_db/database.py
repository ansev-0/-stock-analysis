from src.database.database import DataBaseAdminUsers

class DataBaseUsers(DataBaseAdminUsers):

    def __init__(self, collection):
        super().__init__('users')
        self._collection = collection

    @property
    def collection(self):
        return self._collection

    def list_collection_names(self, *args, **kwargs):
        return self._database.list_collection_names(*args, **kwargs)

    def list_services(self):
        return list(
            filter(lambda collection: 'service' in collection,
                    self.list_collection_names()
                  )
        )
        
class DataBaseUsersGeneralInfo(DataBaseUsers):
    def __init__(self):
        super().__init__('general')
        
class DataBaseUsersService(DataBaseUsers):
    def __init__(self, name_service):
        super().__init__(f'service_{name_service}')


