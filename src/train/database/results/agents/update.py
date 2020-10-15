from src.train.database.results.agents.agent import ResultTrainDataBase

class UpdateResultTrainDataBase(ResultTrainDataBase):

    def update_one(self, where, dict_to_update, **kwargs):
        return self.collection.update_one(where, 
                                          self._update_with_set(dict_to_update), 
                                          **kwargs)

    def update_many(self, where, dict_to_update, **kwargs):
        return self.collection.update_many(where, 
                                           self._update_with_set(dict_to_update),
                                           **kwargs)

    def update_on_id(self, train_id, dict_to_update, **kwargs):
        return self.update_one({'_id' : train_id},
                               dict_to_update, 
                               **kwargs)

    @staticmethod
    def _update_with_set(dict_to_update):
        return {'$set' : dict_to_update}

    
    