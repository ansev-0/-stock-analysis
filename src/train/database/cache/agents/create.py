<<<<<<< HEAD
from src.train.database.chache.agents.agents import DataBaseAgentTrainCache
=======
from src.train.database.cache.agents.agents import DataBaseAgentTrainCache
>>>>>>> ee145a6a2fdce0a7c8f4eea604abe763799e0474
from src.tools.mongodb import encode_array_to_mongodb
import pandas as pd
import numpy as np

class CreateAgentTrainCache(DataBaseAgentTrainCache):

    def __call__(self, **kwargs):
        next_id = self._get_next_id()
        return next_id , \
            self.collection.insert_one({'_id' : next_id,
                                        **self._mapper_params(**kwargs)})

    def _get_next_id(self):
       ids = self._get_ids()
<<<<<<< HEAD
       return self._next_id_from_not_empty(ids) if ids else 0
=======
       return int(self._next_id_from_not_empty(ids)) if ids else 0
>>>>>>> ee145a6a2fdce0a7c8f4eea604abe763799e0474
       
    def _next_id_from_not_empty(self, ids):
        diff_arr = np.setdiff1d(range(len(ids)), ids)
        return diff_arr[0] if diff_arr.size > 0 else len(ids)

    def _get_ids(self):
        return list(map(lambda features: features['_id'], 
                     self.collection.find({}, projection={'id' : 1}))
                )

<<<<<<< HEAD
    def __mapper_params(self, **kwargs):
=======
    def _mapper_params(self, **kwargs):
>>>>>>> ee145a6a2fdce0a7c8f4eea604abe763799e0474
        return {key : self._encode(value) for key, value in kwargs.items()}

    @staticmethod
    def _encode(value):
        if isinstance(value, np.ndarray):
            return encode_array_to_mongodb(value)
        elif isinstance(value, pd.Series):
            return value.to_dict()
        return value
<<<<<<< HEAD
            
=======
>>>>>>> ee145a6a2fdce0a7c8f4eea604abe763799e0474
