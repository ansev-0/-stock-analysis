from src.database.database import DataBaseAdminCronTab

class DataBaseCronTab(DataBaseAdminCronTab):

    def __init__(self, collection):
        super().__init__('crontab')
        self._collection = self._database[collection]

    @property
    def collection(self):
        return self._collection

    def list_collection_names(self, **kwargs):
        return self.collection.list_collection_names(**kwargs)