from src.train.database.cache.agents.find import FindAgentTrainCache

class DecodeStockDataTask:

    _find_sequences = FindAgentTrainCache()
    _projection = {'sequences' : True, '_id' : False, 'time_values' : False}

    def __call__(self, cache_id):
        return self._find_sequences.find_by_id(cache_id, projection=self._projection)


