from src.train.database.cache.agents.agents import DataBaseAgentTrainCache

class FindAgentTrainCache(DataBaseAgentTrainCache):

    ''' MongoDB find wrapper '''
    
    def find_one(self, **kwargs):
        return self.collection.find_one(**kwargs)

    def find_many(self, **kwargs):
        return self.collection.find(**kwargs)

    def find_by_id(self, cache_id, **kwargs):
        return self.collection.find_one({'_id' : cache_id}, **kwargs)
