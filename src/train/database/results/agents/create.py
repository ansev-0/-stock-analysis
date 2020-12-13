from src.train.database.results.agents.agent import ResultTrainDataBase
import numpy as np

class CreateResultTrainDataBase(ResultTrainDataBase):

    def __call__(self, dict_results):
        next_id = self._get_next_id()
        return next_id, self.collection.insert_one({'_id' : next_id, **dict_results})

    def _get_next_id(self):
       ids = self._get_ids()
       return int(self._next_id_from_not_empty(ids)) if ids else 0
       
    def _next_id_from_not_empty(self, ids):
        diff_arr = np.setdiff1d(range(len(ids)), ids)
        return diff_arr[0] if diff_arr.size > 0 else len(ids)

    def _get_ids(self):
        return list(map(lambda features: features['_id'], 
                     self.collection.find({}, projection={'id' : 1}))
        )