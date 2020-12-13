from src.train.database.cache.agents.agents import DataBaseAgentTrainCache

class FindAgentTrainCache(DataBaseAgentTrainCache):

    ''' MongoDB find wrapper '''
    
    def find_one(self, *args, **kwargs):
        return self.collection.find_one(*args, **kwargs)

    def find_many(self, *args, **kwargs):
        return self.collection.find(*args, **kwargs)

    def find_by_id(self, cache_id, **kwargs):
        return self.find_one({'_id' : cache_id}, **kwargs)

    def find_by_ids(self, cache_ids, **kwargs):
        return self.find_many({'_id' : {'$in' : cache_ids}}, **kwargs)
