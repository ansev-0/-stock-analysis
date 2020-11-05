from src.train.database.cache.agents.agents import DataBaseAgentTrainCache

class UpdateAgentTrainCache(DataBaseAgentTrainCache):

    ''' MongoDB update wrapper '''
    
    def update_one(self, where, data, **kwargs):
        return self.collection.update_one(where, self._set_dict(data), **kwargs)

    def update_many(self, where, data, **kwargs):
        return self.collection.update_many(where, self._set_dict(data), **kwargs)

    def update_on_id(self, id, data, **kwargs):
        return self.collection.update_one({'_id' : id},
                                          self._set_dict(data)
                                          **kwargs)
    @staticmethod
    def _set_dict(d):
        return {'$set' : d}

    
