from src.train.database.cache.agents.agents import DataBaseAgentTrainCache

class RemoveAgentTrainCache(DataBaseAgentTrainCache):

    def delete_id(self, id):
        return self.collection.delete_one({'_id' : id})

    def delete_many(self, **kwargs):
        self.collection.delete_many(**kwargs)

    def delete_all(self):
        self.collection.delete_many({})

