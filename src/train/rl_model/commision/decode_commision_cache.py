from src.train.database.cache.agents.find import FindAgentTrainCache
import pandas as pd

class DecodeCommisionCache:

    _find_in_cache = FindAgentTrainCache()

    def __init__(self, type_commisions):
        self.type_commisions = type_commisions


    def __call__(self, dict_cache):
        return tuple(self._decode_param(param, dict_param) for param, dict_param in dict_cache.items())
        
    def _build_serie_from_db(self, cache_id):
        return pd.Series(
            self._find_in_cache.find_by_id(cache_id, 
                                           projection={'time_values' : 1})['time_values'])

    def _decode_param(self, param, dict_param):
        #check valid type commision
        self._check_valid_type_commision(param)
        #get commision value
        return dict_param['value'] * self._build_serie_from_db(dict_param['cache_id']) \
            if 'cache_id' in dict_param else dict_param['value']
        
    def _check_valid_type_commision(self, param):
        if param not in self.type_commisions:
            raise KeyError('Invalid type commision')