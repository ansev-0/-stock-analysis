from src.train.database.cache.agents.find import FindAgentTrainCache
from src.tools.mongodb import decode_array_from_mongodb

class DecodeDataTask:

    _find_sequences = FindAgentTrainCache()
    _projection = {'_id' : 0, 'time_values' : 0}

    def __call__(self, cache_id):
        return decode_array_from_mongodb(
            self._find_sequences.find_by_id(cache_id, projection=self._projection)['sequences']
            )


class DecodeForexDataTask(DecodeDataTask):

    def __call__(self, dict_cache_id):
        l_sequences = []
        for commision in dict_cache_id.values():
            try:
                l_sequences.append(super().__call__(commision['cache_id']))
            except KeyError:
                pass

        return self._output_decoded(l_sequences) if l_sequences else None

    @staticmethod
    def _output_decoded(l_sequences):
        return l_sequences if len(l_sequences) > 1 else l_sequences[0]




