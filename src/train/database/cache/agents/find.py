from src.train.database.cache.agents.agents import DataBaseAgentTrainCache

class FindAgentTrainCache(DataBaseAgentTrainCache):

    ''' MongoDB find wrapper '''
    
    def find_one(self, **kwargs):
        return self.collection.find_one(**kwargs)

    def find_many(self, **kwargs):
        return self.collection.find_many(**kwargs)

    def find_by_id(self, id, **kwargs):
        return self.collection.find_one({'_id' : id}, **kwargs)
