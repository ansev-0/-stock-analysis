from src.assets.database.find import FindAssetInDataBase
from functools import reduce

class TwitterSelectDbToUpdate:

    _find_assets = FindAssetInDataBase()
    
    def __init__(self):
        self._assets = list(self._find_assets.many(False, {}, projection={'_id' : False}))

    def __call__(self, full_text_tweet):

        return [dict_asset['label'] 
                for dict_asset in self._assets
                if any(reduce(lambda cum_list, new_param: self._reduce_func(cum_list, new_param, 
                                                                            full_text_tweet), 
                              dict_asset.values(), [False]))]

    @staticmethod
    def _reduce_func(cum_list, new_param, full_text_tweet):

        if isinstance(new_param, list):
            list_bool = [param in full_text_tweet 
                         for param in new_param 
                         if isinstance(param, str)]
            return cum_list + (list_bool if list_bool else [False])

        elif isinstance(new_param, str):
            return cum_list + [new_param in full_text_tweet]
        else:
            return cum_list + [False]
