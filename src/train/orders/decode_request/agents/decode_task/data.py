from src.train.database.cache.agents.find import FindAgentTrainCache
from src.tools.mongodb import decode_array_from_mongodb
from src.tools.financial import FinancialArray
import pandas as pd

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


class DecodeFinancialDataTask:

    _find_sequences = FindAgentTrainCache()
    _projection_main_frecuency = {'_id' : 0, 'sequences' : 0}
    _projection_financial_data = {'_id' : 0}

    def __call__(self, cache_id, cache_id_main_frecuency):
        index_array, array = self._get_financial_data(cache_id)
        index_of_main_frecuency = self._get_main_index(cache_id_main_frecuency)
        return FinancialArray(array, index_of_main_frecuency, index_array)


    def _get_financial_data(self, cache_id):
        dict_data = self._find_sequences.find_by_id(cache_id, projection=self._projection_financial_data)
        return pd.DatetimeIndex(decode_array_from_mongodb(dict_data['index'])), \
            decode_array_from_mongodb(dict_data['data'])

    def _get_main_index(self, cache_id):
        return pd.DatetimeIndex(list(self._find_sequences.find_by_id(cache_id, projection=self._projection_main_frecuency)['time_values'])[:-1])
