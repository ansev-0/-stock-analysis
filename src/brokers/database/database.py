from src.database.database import DataBaseAdminBrokers


class DataBaseBrokers(DataBaseAdminBrokers):

    def __init__(self, broker):
        super().__init__('brokers')
        self._broker = self._database[broker]

    @property
    def broker(self):
        return self._broker

    def list_brokers(self,  *args, **kwargs):
        return self._database.list_collection_names(*args, **kwargs)
    