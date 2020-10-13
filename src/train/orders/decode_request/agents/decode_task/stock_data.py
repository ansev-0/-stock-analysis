from src.train.database.cache.agents.find import FindAgentTrainCache

class DecodeStockDataTask:

    _find_sequences = FindAgentTrainCache()
    _projection = {'_id' : 0, 'time_values' : 0}

    def __call__(self, cache_id):
        return self._find_sequences.find_by_id(cache_id, projection=self._projection)


