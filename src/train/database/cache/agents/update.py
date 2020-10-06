from src.train.database.cache.agents.agents import DataBaseAgentTrainCache

class UpdateAgentTrainCache(DataBaseAgentTrainCache):

    ''' MongoDB update wrapper '''
    
    def update_one(self, **kwargs):
        return self.collection.update_one(**kwargs)

    def update_many(self, **kwargs):
        return self.collection.update_many(**kwargs)

    def update_on_id(self, id, **kwargs):
        return self.collection.update_one({'_id' : id},
                                          **kwargs)
