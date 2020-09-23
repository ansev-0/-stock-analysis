from src.database.database import DataBaseAdminModels

class DataBaseAgents(DataBaseAdminModels):

    def __init__(self):
        super().__init__('agent')

    def collection_names(self, *args, **kwargs):
        self._database.list_collection_names(*args, **kwargs)


class DataBaseOneAgent(DataBaseAgents):
    def __init__(self, stock_name):
        self.collection = stock_name

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, stock_name):
        self._collection = self._database[stock_name]