from src.brokers.database.database import DataBaseBrokers

class FindBrokers(DataBaseBrokers):

    def find_one(self, *args, **kwargs):
        return self._collection.find_one(*args, **kwargs)

    def find_many(self, *args, **kwargs):
        return self._collection.find(*args, **kwargs)
